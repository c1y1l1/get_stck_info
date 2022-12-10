import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://mops.twse.com.tw/mops/web/t47sb09"
child_co_id = input('請輸入公司代號：')

# 輸入代號，出現詳細資料選項，擷取allow_date
payload_first = {
    'encodeURLComponent':'1',
    'step':'1',
    'firstin':'true',
    'off':'1',
    'keyword4':'',
    'code1':'',
    'TYPEK2':'',
    'checkbtn':'',
    'queryName': child_co_id,
    'inputType': child_co_id,
    'TYPEK':'all',
    'co_id':child_co_id
}

res_first = requests.post(url, data=payload_first, headers=False).content
soup_1 = BeautifulSoup(res_first, 'html.parser')
allow_date = soup_1.find_all('input',value = '詳細資料')[-1]
allow_date = str(allow_date).split('"')[1]

# 透過代號、allow_date，取得表格
payload_second = {
    'TYPEK':'sii',
    'step':'2',
    'co_id':child_co_id,
    'name':'',
    'allow_date':allow_date,
    'type':'',
    'firstin':'true'
}

res_second = requests.post(url, data=payload_second, headers=False).content
soup_2 = BeautifulSoup(res_second, "html.parser")
df_list = pd.read_html(str(soup_2))[11] #表格

file = 'test.csv'
# 基本表格
df_list.iloc[0:4, 0:4].to_csv(file, encoding='big5', mode='a+', index=False, header=False)
# 擷取認股條件
condition = df_list.iloc[11,1]
df_list.iloc[11,1] = condition[condition.find('五、'):condition.find('六、')]
df_list.iloc[11:13,0:2].to_csv(file, encoding='big5', mode='a+', index=False, header=False)


