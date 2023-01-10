import requests
import pandas as pd
from time import gmtime, strftime
from datetime import datetime, timezone, timedelta
from pytz import timezone
from Google import create_service


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


data_uf2=data_uf
data_uf2['fecha'] = pd.to_datetime(data_uf2.fecha)
data_uf2=data_uf2.sort_values(by='fecha',ascending=True)
data_uf2['fecha']=data_uf2['fecha'].dt.strftime('%d/%m/%Y')
data_uf2['valor']=data_uf2['valor'].map('{:,.2f}'.format)
data_uf2 = data_uf2.replace(',', 'x', regex=True)
data_uf2 = data_uf2.replace('\.', ',', regex= True)
data_uf2 = data_uf2.replace('x', '.', regex= True)
data_uf2=data_uf2.drop(columns=['Tipo divisa'])


"""
Getting  Google Sheets
"""
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

services = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,SCOPES )

google_sheets_id = '1iZPHRQNhMk8o7LQzVxkLc7hUnG0NuMFy9Zw1UlVGuS0'

"""
Insert dataset
"""
def construct_request_body(value_array, dimension: str='ROWS') -> dict:
    try:
        request_body = {
            'majorDimension': dimension,
            'values': value_array
        }
        return request_body
    except Exception as e:
        print(e)
        return {}

response = services.spreadsheets().values().get(
    spreadsheetId=google_sheets_id,
    majorDimension='ROWS',
    range='UF'
    ).execute()

def in_list(list1,list2):
    df=pd.DataFrame(columns=['fecha','valor'])
    for i in list1:
        if i not in list2:
            df.loc[len(df)] = i
    return df

df_aux=in_list(data_uf2.values.tolist(),response["values"])

if(len(df_aux)>0):
    request_body_values = construct_request_body(df_aux.values.tolist())
    services.spreadsheets().values().append(
            spreadsheetId=google_sheets_id,
            valueInputOption='USER_ENTERED',
            range="UF",
            body=request_body_values
        ).execute()
    print("UF ingresada en Drive")
else:
    print("Valores ya estan ingresados en Drive")
