import xlrd
from .models import Document
import os

class excel_handling:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def make_file(self, file):
        workbook=xlrd.open_workbook(file_contents=file.read())
        return workbook

    def get_normal(self, workbook):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        normals=[]
        for row_num in range(13, num_rows):
            code=worksheet.cell_value(row_num,1)
            type=worksheet.cell_value(row_num,2)
            if(type=='탁감'):
                data=code+' '+type
                normals.append(data)

        return normals

    def get_code_normal(self, workbook):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        codes=[]
        for row_num in range(13, num_rows):
            code=worksheet.cell_value(row_num,1)
            type = worksheet.cell_value(row_num, 2)
            if (type == '탁감'):
                codes.append(code)

        return codes

    def get_creditor(self, workbook):
        worksheet=workbook.sheet_by_index(0)
        num_rows=worksheet.nrows
        creditors=[]
        for row_num in range(8,num_rows):
            creditor=worksheet.cell_value(row_num,5)
            creditors.append(creditor)

        return creditors
