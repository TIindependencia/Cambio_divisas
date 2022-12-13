import requests
import pandas as pd
from time import gmtime, strftime
from datetime import datetime, timezone, timedelta
import pytz
from pytz import timezone
import pypyodbc as odbc 

year_today = datetime.now(timezone('UTC')).strftime("%Y")
url = "https://mindicador.cl/api/uf/"+year_today
response = requests.get(url)
response = response.json()

data_uf=pd.DataFrame(response["serie"])
data_uf['fecha']=data_uf['fecha'].replace("T03:00:00.000Z","", regex=True)
data_uf['fecha']=data_uf['fecha'].replace("T04:00:00.000Z","", regex=True)
data_uf['fecha']
data_uf["Tipo divisa"]="UF"

now_utc = datetime.now(timezone('UTC'))
date_today = now_utc.astimezone(timezone('America/Santiago')).strftime("%Y-%m-%d")
month_today = now_utc.astimezone(timezone('America/Santiago')).strftime("-%m-")
new_cols = ["Tipo divisa","fecha","valor"]
data_uf=data_uf.reindex(columns=new_cols)
data_uf=data_uf[data_uf['fecha'].str.contains(month_today)]


##conexión a BD

DRIVER_NAME = 'SQL SERVER' 
SERVER_NAME = 'axnew.cindependencia.cl,1569'
DATABASE_NAME = 'GoogleDrive'
UID='DCOBR'
PWD='pago,,1010'; 

def connection_stirng(driver_name, server_name, database_name,uid, pwd):
    conn_string = f"""
        DRIVER={{{driver_name}}};
        SERVER={server_name};
        DATABASE={database_name};
        UID={uid};
        PWD={pwd};   
        Trust_Connection=yes;        
    """
    return conn_string
try:
    conn = odbc.connect(connection_stirng(DRIVER_NAME,SERVER_NAME,DATABASE_NAME,UID,PWD))
    print('Connection created') 
except odbc.DatabaseError as e:
    print('Database Error:')
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error:')
    print(str(e.value[1]))


cursor = conn.cursor() 
cursor.executemany('delete from [GoogleDrive].[dbo].[ExchangeRate]')

sql_insert = '''
    INSERT INTO [GoogleDrive].[dbo].[ExchangeRate]
    VALUES (?, ?, ? )
    '''

records=data_uf.values.tolist()

try:
    cursor = conn.cursor()
    cursor.executemany(sql_insert, records)
    cursor.commit();    
except Exception as e:
    cursor.rollback()
    print(str(e[1]))
finally:
    print('Task is complete.')
    cursor.close()
    conn.close()