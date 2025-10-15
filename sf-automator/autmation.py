
# Optimized automation script with BATCH execution and schema placeholders
import os
import glob
import configparser
import subprocess
import re

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def replace_schema_placeholders(query, config):
    """Replace schema placeholders in SQL with actual schema names from config"""
    first_schema = config['schemas']['1st_schema']
    second_schema = config['schemas']['2nd_schema']
    third_schema = config['schemas']['3rd_schema']
    
    # Replace schema names in the query
    query = re.sub(r'\braw\.', f'{first_schema}.', query)
    query = re.sub(r'\bstage\.', f'{second_schema}.', query)
    query = re.sub(r'\bcurated\.', f'{third_schema}.', query)
    
    return query

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

def execute_all_ddls(config, ddl_root):
    # Get schema names from config
    first_schema = config['schemas']['1st_schema']
    second_schema = config['schemas']['2nd_schema']
    third_schema = config['schemas']['3rd_schema']
    
    # Define the schema execution order using config values
    schema_mapping = {
        'raw': first_schema,
        'stage': second_schema,
        'curated': third_schema
    }
    schema_order = ['raw', 'stage', 'curated']
    
    # Get all table folders
    table_folders = [os.path.join(ddl_root, d) for d in os.listdir(ddl_root) if os.path.isdir(os.path.join(ddl_root, d))]
    table_folders.sort()
    
    print(f"📊 Found {len(table_folders)} table folders")
    print(f"🔄 Execution order: {' -> '.join([schema_mapping[s] for s in schema_order])}")
    print(f"⚡ Using BATCH mode for faster execution")
    print(f"📝 Schema mapping: raw={first_schema}, stage={second_schema}, curated={third_schema}\n")
    
    # Execute by schema order
    for schema_key in schema_order:
        actual_schema = schema_mapping[schema_key]
        print(f"\n{'='*80}")
        print(f"🔷 Executing {actual_schema.upper()} schema objects (from {schema_key} files)")
        print(f"{'='*80}")
        
        # Collect all SQL statements for this schema
        batch_statements = []
        file_names = []
        
        for table_folder in table_folders:
            # Get all SQL files for this schema (using original file prefix)
            sql_files = glob.glob(os.path.join(table_folder, f"{schema_key}.*.sql"))
            
            if not sql_files:
                continue
                
            sql_files.sort()
            
            for sql_file in sql_files:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    query = f.read().strip()
                    if query:
                        # Replace schema names with configured values
                        query = replace_schema_placeholders(query, config)
                        batch_statements.append(query)
                        file_names.append(os.path.basename(sql_file))
        
        if not batch_statements:
            print(f"  ⚠️  No SQL files found for {schema_key} schema")
            continue
        
        print(f"  📦 Batching {len(batch_statements)} DDL statements...")
        
        # Combine all statements with semicolons
        batch_query = ";\n\n".join(batch_statements) + ";"
        
        # Execute the batch
        print(f"  🚀 Executing batch for {actual_schema.upper()} schema...")
        success = run_snowsql_command(config, batch_query)
        
        if success:
            print(f"  ✅ Successfully executed {len(batch_statements)} statements for {actual_schema.upper()} schema")
            for file_name in file_names:
                print(f"    ✓ {file_name}")
        else:
            print(f"  ❌ Batch execution failed for {actual_schema.upper()} schema")
            print(f"  💡 Tip: Check individual files for syntax errors")

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

    # Execute all DDLs
    ddl_root = config['ddl']['ddl_root']
    execute_all_ddls(config, ddl_root)
    
    print(f"\n{'='*80}")
    print("🎉 DDL Execution Complete!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
