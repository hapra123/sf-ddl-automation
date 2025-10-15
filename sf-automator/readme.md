1)Install the Snowsql
2)Install requirements.txt
3)Run the automator
Caution : While using drop_automator it deleted all the views / tables for the respective schema provided

[connection]
account = 
user = 
password = 
warehouse = 
database = 
role = 

[snowsql]
# Path to snowsql executable if needed
snowsql_path = C:\Program Files\Snowflake SnowSQL\snowsql.exe

[ddl]
# Path to DDL folders
ddl_root = d:\Projects\SF-DDL-POC\code\object-creation-scripts\

[schemas]
# Schema names - change these to test with different schemas
1st_schema = 
2nd_schema = 
3rd_schema = 

-------------------------------------------------------------

Change this file to config.ini

Snowsql download path

https://www.snowflake.com/en/developers/downloads/snowsql/

-------------------------------------------------------------