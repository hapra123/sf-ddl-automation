
import os
import configparser
import subprocess

def test_snowsql_connection(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    snowsql_path = config['snowsql']['snowsql_path']
    account = config['connection']['account']
    user = config['connection']['user']
    password = config['connection']['password']
    warehouse = config['connection']['warehouse']
    database = config['connection']['database']
    role = config['connection']['role']
    region = config['connection'].get('region', '')

    # Build SnowSQL connection command
    cmd = [
        snowsql_path,
        '-a', account,
        '-u', user,
        '-w', warehouse,
        '-d', database,
        '-r', role
    ]
    if region:
        cmd.extend(['--region', region])
    cmd.append('-q')
    cmd.append('SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();')

    env = os.environ.copy()
    env['SNOWSQL_PWD'] = password

    print('Running:', ' '.join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    print('STDOUT:')
    print(result.stdout)
    print('STDERR:')
    print(result.stderr)
    return result.returncode == 0

if __name__ == '__main__':
    config_path = 'd:/Projects/SF-DDL-POC/sf-automator/config.ini'
    success = test_snowsql_connection(config_path)
    if success:
        print('Connection successful!')
    else:
        print('Connection failed.')
