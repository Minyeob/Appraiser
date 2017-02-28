import xlrd

class Excel_Handling:
    workbook=xlrd.open_workbook('')

    #파이썬에서 self를 이용해 클래스 내의 속성을 변경시킨다
    def make_excel(self, document):
        self.workbook = xlrd.open_workbook(document)
        return self.workbook

    def get_code(self, workbook):
        #IBK 기준으로 엑셀의 C-1 시트에 코드가 존재
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        codes=[]
        for row_num in range(13, num_rows):
            codes.append(worksheet.cell_value(row_num, 1))
        return codes