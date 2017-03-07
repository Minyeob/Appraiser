import xlrd
from .models import Document
import os

class excel_handling:
    #엑셀파일을 업로드하면 해당 엑셀파일을 읽어 파이썬내에서 처리할 수 있는 형태로 만드는 함수
    def make_file(self, file):
        workbook=xlrd.open_workbook(file_contents=file.read())
        return workbook

    #탁감 데이터들을 모아 선택할 수 있도록 제목을 출력해주는 함수
    def get_normal(self, workbook):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        normals=[]
        program = self.get_program_title(workbook)
        temp = program.split()
        bank = temp[0]
        for row_num in range(13, num_rows):
            type=worksheet.cell_value(row_num,2)
            code=worksheet.cell_value(row_num,1)
            pool = worksheet.cell_value(row_num, 10)
            property = worksheet.cell_value(row_num, 16)
            si_address=worksheet.cell_value(row_num,17)
            gu_address=worksheet.cell_value(row_num,18)
            dong_address=worksheet.cell_value(row_num,19)
            use=worksheet.cell_value(row_num,21)

            if(type=='탁감'):
                data=type+' '+bank+'-'+pool+'-'+property+'-'+si_address+' '+gu_address+' '+dong_address+'-'+use
                normals.append(data)

        return normals

    #탁감 데이터들의 코드를 출력하는 함수
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

    #차주들을 구해 출력해주는 함수
    def get_borrower(self, workbook, loc):
        worksheet=workbook.sheet_by_index(2)
        num_rows=worksheet.nrows
        borrowers=[]
        for row_num in range(13,num_rows):
            creditor=worksheet.cell_value(row_num,13)
            borrowers.append(creditor)
        borrower=borrowers[loc]
        return borrower

    #모든 형태의 데이터의 코드들을 출력해주는 함수
    def get_code_all(self, workbook):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        codes = []
        for row_num in range(13, num_rows):
            code = worksheet.cell_value(row_num, 1)
            codes.append(code)

        return codes

    #해당 엑셀파일의 Program 이름을 출력해주는 함수
    def get_program_title(self, workbook):
        worksheet=workbook.sheet_by_index(0)
        program_title=worksheet.cell_value(1,0)

        return program_title

    #선택된 데이터의 property control no 를 출력해주는 함수
    def get_property_control(self, workbook, loc):
        worksheet=workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        program=self.get_program_title(workbook)
        temp=program.split()
        bank=temp[0]
        pools=[]
        for row_num in range(13, num_rows):
            pool = worksheet.cell_value(row_num, 10)
            pools.append(pool)
        pool=pools[loc]
        properties=[]
        for row_num in range(13, num_rows):
            property = worksheet.cell_value(row_num, 16)
            properties.append(property)
        property_code=properties[loc]
        control_no=bank+'-'+pool+'-'+property_code

        return control_no

    #각 데이터의 분류들을 모아 출력해주는 함수
    def get_type(self, workbook):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        types = []
        for row_num in range(13, num_rows):
            type = worksheet.cell_value(row_num, 2)
            types.append(type)

        return types

    #선택된 데이터의 관할법원을 출력해주는 함수
    def get_court(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        courts = []
        for row_num in range(13, num_rows):
            court = worksheet.cell_value(row_num, 72)
            courts.append(court)

        court=courts[loc]
        return court

    #선택된 데이터의 사건번호를 출력해주는 함수
    def get_case_number(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        case_numbers = []
        for row_num in range(13, num_rows):
            case = worksheet.cell_value(row_num, 73)
            case_numbers.append(case)

        case = case_numbers[loc]
        return case

    #선택된 데이터의 Borrow Name을 출력해주는 함수
    def get_borrower_num(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        borrower_nums = []
        for row_num in range(13, num_rows):
            borrower = worksheet.cell_value(row_num, 12)
            borrower_nums.append(borrower)

        borrower=borrower_nums[loc]
        return borrower

    #선택된 데이터의 OPB를 출력해주는 함수
    def get_opb(self, workbook, bnum):
        worksheet = workbook.sheet_by_index(0)
        num_rows = worksheet.nrows
        for row_num in range(8, num_rows):
            borrower = worksheet.cell_value(row_num, 4)
            opb=worksheet.cell_value(row_num, 13)
            if(borrower==bnum):
                result=opb

        return result

    #선택된 데이터의 연체이자를 출력해주는 함수
    def get_overdue_interest(self, workbook, bnum):
        worksheet = workbook.sheet_by_index(0)
        num_rows = worksheet.nrows
        for row_num in range(8, num_rows):
            borrower = worksheet.cell_value(row_num, 4)
            interest = worksheet.cell_value(row_num, 14)
            if (borrower == bnum):
                result = interest

        return result

    #선택된 데이터의 설정액을 출력해주는 함수
    def get_setup_price(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        prices = []
        for row_num in range(13, num_rows):
            setup_price = worksheet.cell_value(row_num, 30)
            prices.append(setup_price)

        setup_price = prices[loc]
        return setup_price

    #선택된 데이터의 총 주소를 출력해주는 함수
    def get_full_address(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        address=[]
        for row_num in range(13, num_rows):
            si_address = worksheet.cell_value(row_num, 17)
            gu_address = worksheet.cell_value(row_num, 18)
            dong_address = worksheet.cell_value(row_num, 19)
            remain = worksheet.cell_value(row_num, 20)
            remains=remain.split(',')
            if(len(remains)>1):
                remain_address=remains[0]+ '외 '+ str(len(remains)-1)+ '개호'
            else:
                remain_address=remains[0]

            full_address=si_address+' '+gu_address+' '+dong_address+' '+remain_address
            address.append(full_address)

        result=address[loc]
        return result

    def get_property_category(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        categories = []
        for row_num in range(13, num_rows):
            use = worksheet.cell_value(row_num, 21)
            categories.append(use)

        property_category=categories[loc]
        return property_category
