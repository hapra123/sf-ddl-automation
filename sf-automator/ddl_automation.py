# DDL automation script - Direct execution without schema replacement
import os
import glob
import configparser
import subprocess
import time

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def run_snowsql_command(config, query):
    snowsql_path = config['snowsql']['snowsql_path']
    account = config['connection']['account']
    user = config['connection']['user']
    password = config['connection']['password']
    warehouse = config['connection']['warehouse']
    database = config['connection']['database']
    role = config['connection']['role']

    env = os.environ.copy()
    env['SNOWSQL_PWD'] = password

    cmd = [
        snowsql_path,
        '-a', account,
        '-u', user,
        '-w', warehouse,
        '-d', database,
        '-r', role,
        '-q', query
    ]

    print(f"Running: {' '.join(cmd[:7])}... [query hidden]")
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    print("STDOUT:")
    print(result.stdout)
    
    has_errors = False
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        # Check if stderr contains actual SQL errors (not just warnings)
        if 'SQL compilation error' in result.stderr or 'does not exist' in result.stderr or result.returncode != 0:
            has_errors = True
    
    # Return success only if no errors and exit code is 0
    return result.returncode == 0 and not has_errors

def extract_schema_from_file(file_content):
    """Extract the schema name used in the SQL file"""
    import re
    # Look for CREATE TABLE/VIEW schema.object_name patterns
    patterns = [
        r'CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\s+(\w+)\.',
        r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+(\w+)\.',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, file_content, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    return None

def execute_schema_files(config, ddl_root, file_prefix, target_schema):
    """Execute DDL files with specific prefix for a target schema"""
    start_time = time.time()
    
    print(f"\n{'='*80}")
    print(f"🔷 Executing {target_schema.upper()} schema objects (from {file_prefix}.* files)")
    print(f"{'='*80}")
    
    # Get all table folders
    table_folders = [os.path.join(ddl_root, d) for d in os.listdir(ddl_root) if os.path.isdir(os.path.join(ddl_root, d))]
    table_folders.sort()
    
    # Collect all SQL statements for this file prefix
    batch_statements = []
    file_info = []  # Store file name and detected schema
    schema_mismatch_found = False
    
    for table_folder in table_folders:
        # Get all SQL files for this prefix
        sql_files = glob.glob(os.path.join(table_folder, f"{file_prefix}.*.sql"))
        
        if not sql_files:
            continue
            
        sql_files.sort()
        
        for sql_file in sql_files:
            with open(sql_file, 'r', encoding='utf-8') as f:
                query = f.read().strip()
                if query:
                    # Extract schema from SQL content
                    detected_schema = extract_schema_from_file(query)
                    file_name = os.path.basename(sql_file)
                    
                    # CRITICAL VALIDATION: File prefix must match detected schema
                    if detected_schema and detected_schema.lower() != file_prefix.lower():
                        print(f"  ❌ SCHEMA MISMATCH: {file_name}")
                        print(f"     File prefix: '{file_prefix}' but SQL creates objects in '{detected_schema}' schema")
                        print(f"     Expected: {file_prefix}.* files should only create objects in '{file_prefix}' schema")
                        schema_mismatch_found = True
                        continue
                    
                    # Validate: file prefix should match target schema intent
                    # But SQL content can use any schema name as written
                    if detected_schema:
                        file_info.append({
                            'name': file_name,
                            'prefix': file_prefix,
                            'detected_schema': detected_schema,
                            'query': query
                        })
                        batch_statements.append(query)
                    else:
                        print(f"  ⚠️  Warning: Could not detect schema in {file_name}")
                        batch_statements.append(query)
                        file_info.append({
                            'name': file_name,
                            'prefix': file_prefix,
                            'detected_schema': 'unknown',
                            'query': query
                        })
    
    # Stop if schema mismatch found
    if schema_mismatch_found:
        print(f"\n  🛑 Stopping execution due to schema mismatches")
        print(f"  💡 Tip: File prefix must match the schema used in SQL statements")
        return False, 0, 0
    
    if not batch_statements:
        print(f"  ⚠️  No SQL files found with prefix '{file_prefix}'")
        return False, 0, 0
    
    print(f"  ✅ Validation passed: All {len(batch_statements)} file(s) use correct schema '{file_prefix}'")
    print(f"  📋 Files to execute:")
    for info in file_info:
        print(f"     ✓ {info['name']} → {info['detected_schema']} schema")
    
    # Combine all statements with semicolons
    batch_query = ";\n\n".join(batch_statements) + ";"
    
    # Execute the batch
    print(f"\n  🚀 Executing batch for {target_schema.upper()} schema...")
    success = run_snowsql_command(config, batch_query)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        print(f"  ✅ Successfully executed {len(batch_statements)} statement(s)")
        print(f"  ⏱️  Execution time: {duration:.2f} seconds")
    else:
        print(f"  ❌ Batch execution failed")
        print(f"  💡 Tip: Check that '{target_schema}' schema exists and SQL syntax is correct")
    
    return success, len(batch_statements), duration

def display_menu(available_schemas):
    """Display menu for schema selection"""
    print(f"\n{'='*80}")
    print("📋 SCHEMA EXECUTION MENU")
    print(f"{'='*80}")
    
    idx = 1
    for schema_info in available_schemas:
        print(f"  {idx}. Execute {schema_info['name'].upper()} schema ({schema_info['prefix']}.* files)")
        idx += 1
    
    print(f"  0. Exit")
    print(f"{'='*80}")
    print(f"\n💡 Note: Files are executed AS-IS. Schema names in SQL files are NOT modified.")

def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = load_config(config_path)

    # Test connection
    print("🔌 Testing Snowflake connection...")
    query = "SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();"
    success = run_snowsql_command(config, query)
    if success:
        print("✅ Connection successful!\n")
    else:
        print("❌ Connection failed.")
        return

    # Build available schemas list
    available_schemas = [
        {'name': config['schemas']['1st_schema'], 'prefix': config['schemas']['1st_schema']},
        {'name': config['schemas']['2nd_schema'], 'prefix': config['schemas']['2nd_schema']},
        {'name': config['schemas']['3rd_schema'], 'prefix': config['schemas']['3rd_schema']},
    ]
    
    ddl_root = config['ddl']['ddl_root']
    
    # Get all table folders for display
    table_folders = [os.path.join(ddl_root, d) for d in os.listdir(ddl_root) if os.path.isdir(os.path.join(ddl_root, d))]
    print(f"📊 Found {len(table_folders)} table folders\n")
    
    while True:
        # Display menu
        display_menu(available_schemas)
        
        # Get user selection
        try:
            choice = int(input("\nEnter your choice: ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue
        
        if choice == 0:
            print("\n👋 Exiting...")
            break
        
        if choice < 1 or choice > len(available_schemas):
            print("❌ Invalid choice.")
            continue
        
        # Track execution stats
        overall_start = time.time()
        execution_results = []
        
        # Execute the selected schema
        schemas_to_execute = [available_schemas[choice - 1]]
        
        # Execute selected schemas
        print(f"\n⚡ Executing {len(schemas_to_execute)} schema(s)...")
        
        all_success = True
        total_files = 0
        
        for schema_info in schemas_to_execute:
            success, file_count, duration = execute_schema_files(
                config, 
                ddl_root, 
                schema_info['prefix'], 
                schema_info['name']
            )
            
            execution_results.append({
                'schema': schema_info['name'],
                'prefix': schema_info['prefix'],
                'success': success,
                'file_count': file_count,
                'duration': duration
            })
            
            total_files += file_count
            
            if not success:
                all_success = False
                print(f"\n🛑 Execution stopped due to failure")
                break
        
        # Calculate overall time
        overall_end = time.time()
        overall_duration = overall_end - overall_start
        
        # Print summary only if all succeeded
        if all_success and total_files > 0:
            print(f"\n{'='*80}")
            print("📊 EXECUTION SUMMARY")
            print(f"{'='*80}")
            
            for result in execution_results:
                if result['file_count'] > 0:
                    time_per_file = result['duration'] / result['file_count']
                    status = '✅' if result['success'] else '❌'
                    print(f"  {status} {result['schema'].upper()}: {result['duration']:.2f}s | {result['file_count']} files | {time_per_file:.2f}s per file")
            
            print(f"\n  📁 TOTAL FILES EXECUTED: {total_files}")
            print(f"  ⏱️  TOTAL EXECUTION TIME: {overall_duration:.2f} seconds ({overall_duration/60:.2f} minutes)")
            print(f"  ⚡ AVERAGE TIME PER FILE: {overall_duration/total_files:.2f} seconds")
            
            print(f"{'='*80}")
            print("\n🎉 Execution Complete!")
        
        # Ask if user wants to continue
        continue_choice = input("\nRun another execution? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
