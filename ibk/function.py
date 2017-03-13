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
    def get_normal_code(self, workbook):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        codes=[]
        for row_num in range(13, num_rows):
            code=worksheet.cell_value(row_num,1)
            type = worksheet.cell_value(row_num, 2)
            if (type == '탁감'):
                codes.append(code)

        return codes

    #차주명을 구해 출력해주는 함수
    def get_render_name(self, workbook, loc):
        worksheet=workbook.sheet_by_index(2)
        num_rows=worksheet.nrows
        renders=[]
        for row_num in range(13,num_rows):
            creditor=worksheet.cell_value(row_num,13)
            renders.append(creditor)
        render=renders[loc]
        return render

    #모든 형태(탁감,정밀,아파트 등)의 데이터의 코드들을 출력해주는 함수
    def get_all_code(self, workbook):
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
    def get_property_control_no(self, workbook, loc):
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

        case_number = case_numbers[loc]
        return case_number

    #선택된 데이터의 차주일련번호를 출력해주는 함수
    def get_render_index(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        borrower_nums = []
        for row_num in range(13, num_rows):
            borrower = worksheet.cell_value(row_num, 12)
            borrower_nums.append(borrower)

        render_index=borrower_nums[loc]
        return render_index

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
    def get_accured_interest(self, workbook, bnum):
        worksheet = workbook.sheet_by_index(0)
        num_rows = worksheet.nrows
        for row_num in range(8, num_rows):
            borrower = worksheet.cell_value(row_num, 4)
            interest = worksheet.cell_value(row_num, 14)
            if (borrower == bnum):
                result = interest

        return result

    #선택된 데이터의 설정액을 출력해주는 함수
    def get_cpma(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        prices = []
        for row_num in range(13, num_rows):
            setup_price = worksheet.cell_value(row_num, 30)
            prices.append(setup_price)

        cpma = prices[loc]
        return cpma

    #선택된 데이터의 총 주소를 출력해주는 함수
    def get_address(self, workbook, loc, code):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        address=[]
        ho=self.get_ho(workbook, code)
        for row_num in range(13, num_rows):
            province = worksheet.cell_value(row_num, 17)
            city = worksheet.cell_value(row_num, 18)
            district = worksheet.cell_value(row_num, 19)
            addtdistrict = worksheet.cell_value(row_num, 20)
            if(len(ho)>1):
                addtdistrict=addtdistrict+'외'

            full_address=province+' '+city+' '+district+' '+addtdistrict
            address.append(full_address)

        result=address[loc]
        return result

    #해당 건물의 용도를 구해 return 해주는 함수
    def get_property_category(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        categories = []
        for row_num in range(13, num_rows):
            use = worksheet.cell_value(row_num, 21)
            categories.append(use)

        property_category=categories[loc]
        return property_category

    #추가적인 건물의 호수들을 return 해주는 함수
    def get_ho(self, workbook, code):
        worksheet=workbook.sheet_by_index(3)
        num_rows = worksheet.nrows
        result=[]
        for row_num in range(8, num_rows):
            number=worksheet.cell_value(row_num,8)
            ho=worksheet.cell_value(row_num, 13)
            if(number==code):
                result.append(ho)

        return result

    #추가적인 건물의 전용적인 면적(건물면적)을 return 해주는 함수
    def get_liensize_improvement(self, workbook, code):
        worksheet = workbook.sheet_by_index(3)
        num_rows = worksheet.nrows
        result = []
        for row_num in range(8, num_rows):
            number = worksheet.cell_value(row_num, 8)
            size = worksheet.cell_value(row_num, 16)
            if (number == code):
                result.append(size)

        return result

    #추가적인 건물의 대지권의 면적을 return 해주는 함수
    def get_landsize(self, workbook, code):
        worksheet=workbook.sheet_by_index(3)
        num_rows=worksheet.nrows
        result=[]
        for row_num in range(8, num_rows):
            number=worksheet.cell_value(row_num,8)
            liensize_land=worksheet.cell_value(row_num, 15)
            land_ratio=worksheet.cell_value(row_num, 17)
            if (number == code):
                if(land_ratio):
                    result.append(liensize_land*land_ratio)

        return result

    #기계들의 개수가 얼마나 되는지 return 해주는 함수
    def get_utensil(self, workbook, loc):
        worksheet = workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        numbers = []
        for row_num in range(13, num_rows):
            number = worksheet.cell_value(row_num, 24)
            if(number=='상기일괄'):
                i=row_num
                while(number=='상기일괄'):
                    i=i-1
                    number=worksheet.cell_value(i,24)
                numbers.append(number)
            else:
                numbers.append(number)

        utensil = numbers[loc]
        return utensil

    #해당 사건의 주소에 대한 법정동코드를 return 해준다
    def get_address_code(self, workbook, loc):
        worksheet=workbook.sheet_by_index(2)
        num_rows = worksheet.nrows
        addresses=[]
        #엑셀파일에서 자신이 칮고자 하는 주소를 구한다
        for row_num in range(13, num_rows):
            province = worksheet.cell_value(row_num, 17)
            city = worksheet.cell_value(row_num, 18)
            district = worksheet.cell_value(row_num, 19)
            full_address = province + ' ' + city + ' ' + district
            addresses.append(full_address)

        address=addresses[loc]

        #법정동코드 엑셀파일을 연다
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        file_path = os.path.join(MEDIA_ROOT, 'address_code.xlsx')
        code_workbook=xlrd.open_workbook(file_path)
        code_worksheet=code_workbook.sheet_by_index(0)
        num_rows = code_worksheet.nrows

        #내가 찾고자 하는 주소의 법정동코드를 구해 return 해준다
        for row_num in range(1,num_rows):
            code=code_worksheet.cell_value(row_num,0)
            goal=code_worksheet.cell_value(row_num,1)
            if(goal==address):
                return int(code)

        return None