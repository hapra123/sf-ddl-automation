# Drop automation script for Snowflake schema objects
import os
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
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    return result.returncode == 0

def get_schema_objects(config, schema_name):
    """Get all tables and views from the specified schema"""
    print(f"\n🔍 Fetching objects from {schema_name.upper()} schema...")
    
    # Query to get all tables
    tables_query = f"""
    SELECT TABLE_NAME, TABLE_TYPE 
    FROM {config['connection']['database']}.INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = '{schema_name.upper()}'
    ORDER BY TABLE_TYPE, TABLE_NAME;
    """
    
    success = run_snowsql_command(config, tables_query)
    
    if success:
        print(f"✅ Successfully retrieved object list from {schema_name.upper()} schema")
    else:
        print(f"❌ Failed to retrieve objects from {schema_name.upper()} schema")
    
    return success

def drop_objects_by_type(config, schema_name, object_type):
    """Drop all objects of a specific type (TABLE or VIEW) from the schema"""
    start_time = time.time()
    
    print(f"\n{'='*80}")
    print(f"🗑️  Dropping all {object_type}s from {schema_name.upper()} schema")
    print(f"{'='*80}")
    
    # Get list of objects to drop
    if object_type.upper() == 'VIEW':
        list_query = f"""
        SELECT TABLE_NAME
        FROM {config['connection']['database']}.INFORMATION_SCHEMA.VIEWS 
        WHERE TABLE_SCHEMA = '{schema_name.upper()}';
        """
    else:  # TABLE
        list_query = f"""
        SELECT TABLE_NAME
        FROM {config['connection']['database']}.INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = '{schema_name.upper()}' AND TABLE_TYPE = 'BASE TABLE';
        """
    
    print(f"📋 Listing {object_type}s...")
    
    # Get object names
    result = subprocess.run(
        [
            config['snowsql']['snowsql_path'],
            '-a', config['connection']['account'],
            '-u', config['connection']['user'],
            '-w', config['connection']['warehouse'],
            '-d', config['connection']['database'],
            '-r', config['connection']['role'],
            '-q', list_query,
            '-o', 'output_format=plain',
            '-o', 'friendly=false',
            '-o', 'timing=false',
            '-o', 'header=false'
        ],
        capture_output=True,
        text=True,
        env={**os.environ, 'SNOWSQL_PWD': config['connection']['password']}
    )
    
    # Extract object names from output
    object_names = []
    for line in result.stdout.split('\n'):
        line = line.strip()
        if line and not line.startswith('*') and not line.startswith('+') and line != 'Goodbye!':
            # Remove any extra whitespace or separators
            clean_name = line.strip('| ').strip()
            if clean_name:
                object_names.append(clean_name)
    
    if not object_names:
        print(f"ℹ️  No {object_type}s found in {schema_name.upper()} schema")
        return True
    
    print(f"📦 Found {len(object_names)} {object_type}(s) to drop:")
    for name in object_names:
        print(f"    - {name}")
    
    # Build DROP statements
    drop_statements = []
    for obj_name in object_names:
        if object_type.upper() == 'VIEW':
            drop_statements.append(f"DROP VIEW IF EXISTS {schema_name}.{obj_name};")
        else:
            drop_statements.append(f"DROP TABLE IF EXISTS {schema_name}.{obj_name} CASCADE;")
    
    # Execute all DROP statements in batch
    print(f"\n🗑️  Executing DROP statements...")
    batch_drop = "\n".join(drop_statements)
    success = run_snowsql_command(config, batch_drop)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        print(f"✅ Successfully dropped {len(drop_statements)} {object_type}(s)")
        print(f"⏱️  Execution time: {duration:.2f} seconds")
    else:
        print(f"❌ Failed to drop some {object_type}s")
    
    return success

def drop_all_objects(config, schema_name):
    """Drop all objects (views first, then tables) from the schema"""
    overall_start = time.time()
    
    print(f"\n{'='*80}")
    print(f"🗑️  DROPPING ALL OBJECTS FROM {schema_name.upper()} SCHEMA")
    print(f"{'='*80}")
    
    # Drop views first (they depend on tables)
    print("\n🔷 Step 1: Dropping VIEWS...")
    views_success = drop_objects_by_type(config, schema_name, 'VIEW')
    
    if not views_success:
        print("\n⚠️  Warning: Failed to drop views, but continuing...")
    
    # Then drop tables
    print("\n🔷 Step 2: Dropping TABLES...")
    tables_success = drop_objects_by_type(config, schema_name, 'TABLE')
    
    overall_end = time.time()
    overall_duration = overall_end - overall_start
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 DROP SUMMARY")
    print(f"{'='*80}")
    print(f"  Schema: {schema_name.upper()}")
    print(f"  Views: {'✅ Dropped' if views_success else '❌ Failed'}")
    print(f"  Tables: {'✅ Dropped' if tables_success else '❌ Failed'}")
    print(f"  ⏱️  Total time: {overall_duration:.2f} seconds")
    print(f"{'='*80}")

def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = load_config(config_path)
    
    # Get schema to drop from config
    if 'drop' not in config:
        print("❌ Error: [drop] section not found in config.ini")
        print("💡 Please add the following to your config.ini:")
        print("\n[drop]")
        print("target_schema = raw")
        return
    
    target_schema = config['drop'].get('target_schema', '').strip()
    
    if not target_schema:
        print("❌ Error: target_schema not specified in [drop] section")
        return
    
    # Test connection
    print("🔌 Testing Snowflake connection...")
    query = "SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();"
    success = run_snowsql_command(config, query)
    if not success:
        print("❌ Connection failed.")
        return
    print("✅ Connection successful!\n")
    
    # Show schema info
    get_schema_objects(config, target_schema)
    
    # Confirmation prompt
    print(f"\n{'='*80}")
    print(f"⚠️  WARNING: You are about to DROP ALL OBJECTS from '{target_schema.upper()}' schema!")
    print(f"{'='*80}")
    confirmation = input(f"\nType 'DELETE {target_schema.upper()}' to confirm: ")
    
    if confirmation != f'DELETE {target_schema.upper()}':
        print("\n❌ Drop operation cancelled.")
        return
    
    # Ask what to drop
    print("\nWhat would you like to drop?")
    print("  1. Only VIEWS")
    print("  2. Only TABLES")
    print("  3. ALL OBJECTS (Views + Tables)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == '1':
        drop_objects_by_type(config, target_schema, 'VIEW')
    elif choice == '2':
        drop_objects_by_type(config, target_schema, 'TABLE')
    elif choice == '3':
        drop_all_objects(config, target_schema)
    else:
        print("❌ Invalid choice. Operation cancelled.")
        return
    
    print("\n🎉 Drop operation complete!")

if __name__ == "__main__":
    main()
