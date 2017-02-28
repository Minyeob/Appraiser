import xlrd
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='12345',
                       db='testdb', charset='utf8')
cursor = conn.cursor()

workbook=xlrd.open_workbook('ibk.xlsx')
worksheet=workbook.sheet_by_index(2)
worksheet_next=workbook.sheet_by_index(1)
num_rows=worksheet.nrows
num_column=worksheet.ncols



usd_currency=worksheet.cell_value(8,29)
jpy_currency=worksheet.cell_value(8,30)

print(usd_currency)
print(jpy_currency)

#여러가지 화폐로 작성된 금액을 KRW로 계산한 결과
prices=[]
for row_num in range(13,num_rows):
    temp=worksheet.cell_value(row_num,29)
    if(type(temp)==str):
        multi=[]
        sum=0
        multi=temp.split()
        print(multi)
        for i in range(0,len(multi)):
            multi[i]=multi[i].replace(',','')
        for num in range(0,len(multi),2):
            if(multi[num]=='USD'):
                sum=sum+float(multi[num+1])*usd_currency
            elif(multi[num]=='JPY'):
                sum=sum+float(multi[num+1])*jpy_currency
            elif(multi[num]=='KRW'):
                sum=sum+float(multi[num+1])
        print(sum)
        temp=sum
    prices.append(temp)
print(prices)

#엑셀에서 퍼센트로 표시되있는 데이터는 1이하의 소수점값으로 표시가 된다 퍼센트 단위로 출력하기 위해서는 100을 곱하고 퍼센트를 붙이면 된다
print(str(worksheet_next.cell_value(100,12)*100)+"%")