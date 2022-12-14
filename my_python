import requests
import pandas as pd
from time import gmtime, strftime
from datetime import datetime, timezone, timedelta
import pytz
from pytz import timezone
import pyodbc

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
DRIVER_NAME = 'ODBC Driver 18 for SQL Server'
SERVER_NAME = '192.168.1.31,1433'
DATABASE_NAME = 'GoogleDrive'
UID='google'
PWD='Pago1010.'; 

try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+SERVER_NAME+';DATABASE='+DATABASE_NAME+';ENCRYPT=no;UID='+UID+';PWD='+ PWD +'')
    print('Connection created') 
except pyodbc.DatabaseError as e:
    print('Database Error 1:')
    print(str(e.value[1]))
except pyodbc.Error as e:
    print('Connection Error 2:')
    print(str(e.value[1]))


cursor = conn.cursor() 
cursor.execute("delete from GoogleDrive.dbo.ExchangeRate") 
cursor.execute("INSERT INTO [dbo].[ExecuteDocker]([Tabla],[Fecha]) VALUES ('ExchangeRate',GETDATE())") 

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