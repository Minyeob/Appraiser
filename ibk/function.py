import xlrd
from .models import Document
import os
import xlutils.copy
import re

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
            ho=str(worksheet.cell_value(row_num, 13))
            arr=ho.split()
            end=len(arr)

            if(number==code):
                temp = int(re.findall('\d+', arr[end-1])[0])
                result.append(temp)

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
            value=0
            if (number == code):
                if(land_ratio):
                    value=liensize_land*land_ratio
            result.append(value)
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

class excel_write:
    def getOutCell(self, outSheet, colIndex, rowIndex):
        """ HACK: Extract the internal xlwt cell representation. """
        row = outSheet._Worksheet__rows.get(rowIndex)
        if not row: return None

        cell = row._Row__cells.get(colIndex)
        return cell

    def setOutCell(self, outSheet, col, row, value):
        """ Change cell value without changing formatting. """
        # HACK to retain cell style.
        previousCell = self.getOutCell(outSheet, col, row)
        # END HACK, PART I

        outSheet.write(row, col, value)

        # HACK, PART II
        if previousCell:
            newCell = self.getOutCell(outSheet, col, row)
            if newCell:
                newCell.xf_idx = previousCell.xf_idx
        # END HACK

    def set_new_cell(self, outSheet, precol, prerow, col, row, value):
        previousCell = self.getOutCell(outSheet, precol, prerow)
        outSheet.write(row, col, value)

        if previousCell:
            newCell = self.getOutCell(outSheet, col, row)
            if newCell:
                newCell.xf_idx = previousCell.xf_idx


    def save_file(self, user_input):
        print(user_input)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        file_path = os.path.join(MEDIA_ROOT, 'output_sample.xls')
        inbook = xlrd.open_workbook(file_path, formatting_info=True)
        outbook = xlutils.copy.copy(inbook)
        outsheet=outbook.get_sheet(0)

        #결과요약
        self.setOutCell(outsheet, 11, 3, user_input['program'])
        self.setOutCell(outsheet, 32, 3, user_input['opb'])
        self.setOutCell(outsheet, 11, 4, user_input['user'])
        self.setOutCell(outsheet, 32, 4, user_input['interest'])
        self.setOutCell(outsheet, 11, 5, user_input['user_phone'])
        self.setOutCell(outsheet, 32, 5, user_input['credit_amount'])
        self.setOutCell(outsheet, 11, 6, user_input['property_control_no'])
        self.setOutCell(outsheet, 32, 6, user_input['setup_price'])
        self.setOutCell(outsheet, 11, 7, user_input['borrow_name'])
        self.setOutCell(outsheet, 32, 7, user_input['law_price'])
        self.setOutCell(outsheet, 11, 8, user_input['market_predict'])
        self.setOutCell(outsheet, 32, 8, user_input['market_price'])
        self.setOutCell(outsheet, 11, 9, user_input['court'])
        self.setOutCell(outsheet, 32, 9, user_input['bid'])
        self.setOutCell(outsheet, 11, 10, user_input['case'])
        self.setOutCell(outsheet, 32, 10, user_input['avg_bid'])
        self.setOutCell(outsheet, 11, 11, user_input['submission_date'])
        self.setOutCell(outsheet, 32, 11, user_input['next_date'])

        self.setOutCell(outsheet, 40, 8, user_input['law_price_comp1'])
        self.setOutCell(outsheet, 44, 8, user_input['market_price_comp1'])
        self.setOutCell(outsheet, 48, 8, user_input['opb_comp1'])
        self.setOutCell(outsheet, 40, 9, user_input['law_price_comp2'])
        self.setOutCell(outsheet, 44, 9, user_input['market_price_comp2'])
        self.setOutCell(outsheet, 48, 9, user_input['opb_comp2'])
        self.setOutCell(outsheet, 40, 10, user_input['law_price_comp3'])
        self.setOutCell(outsheet, 44, 10, user_input['market_price_comp3'])
        self.setOutCell(outsheet, 48, 10, user_input['opb_comp3'])
        self.setOutCell(outsheet, 46, 11, user_input['fail_count'])

        #본건현황
        self.setOutCell(outsheet, 55, 4, user_input['address'])
        self.setOutCell(outsheet, 91, 4, user_input['property_category'])
        self.setOutCell(outsheet, 55, 7, user_input['usage'])
        self.setOutCell(outsheet, 60, 7, user_input['land_category'])
        self.setOutCell(outsheet, 64, 7, user_input['state'])
        self.setOutCell(outsheet, 69, 7, user_input['land_price_m'])
        self.setOutCell(outsheet, 75, 7, user_input['land_price_py'])
        self.setOutCell(outsheet, 82, 7, user_input['land_size_m'])
        self.setOutCell(outsheet, 88, 7, user_input['land_size_py'])
        self.setOutCell(outsheet, 94, 7, user_input['security_size_m'])
        self.setOutCell(outsheet, 100, 7, user_input['security_size_py'])

        self.setOutCell(outsheet, 55, 10, user_input['structure'])
        self.setOutCell(outsheet, 62, 10, user_input['permission_date'])
        self.setOutCell(outsheet, 69, 10, user_input['floor_usage'])
        self.setOutCell(outsheet, 78, 10, user_input['exclusive_rate'])
        self.setOutCell(outsheet, 82, 10, user_input['exclusive_area_m'])
        self.setOutCell(outsheet, 88, 10, user_input['exclusive_area_py'])
        self.setOutCell(outsheet, 94, 10, user_input['contract_area_m'])
        self.setOutCell(outsheet, 100, 10, user_input['contract_area_py'])

        #건물
        building_count=len(user_input['building_ho'])
        height=16
        for index in range(0,building_count):
            print(user_input['building_label'][index])
            self.set_new_cell(outsheet, 2, 16, 2, height+index, user_input['building_label'][index])
            self.set_new_cell(outsheet, 5, 16, 5, height + index, user_input['building_ho'][index])
            self.set_new_cell(outsheet, 9, 16, 9, height + index, round(float(user_input['building_exclusive_m'][index]),2))
            self.set_new_cell(outsheet, 13, 16, 13, height + index, round(float(user_input['building_exclusive_py'][index]), 2))
            self.set_new_cell(outsheet, 17, 16, 17, height + index, round(float(user_input['building_contract_m'][index]), 2))
            self.set_new_cell(outsheet, 21, 16, 21, height + index, round(float(user_input['building_contract_py'][index]), 2))
            self.set_new_cell(outsheet, 25, 16, 25, height + index, round(float(user_input['building_right_m'][index]), 2))
            self.set_new_cell(outsheet, 29, 16, 29, height + index, round(float(user_input['building_right_py'][index]), 2))
            self.set_new_cell(outsheet, 33, 16, 33, height+index, user_input['building_ratio'][index])
            self.set_new_cell(outsheet, 37, 16, 37, height + index, user_input['building_auction_price'][index])
            self.set_new_cell(outsheet, 44, 16, 44, height + index, user_input['building_auction_exclusive'][index])
            self.set_new_cell(outsheet, 50, 16, 50, height + index, user_input['building_auction_contract'][index])
            self.set_new_cell(outsheet, 56, 16, 56, height + index, user_input['building_auction_ratio'][index])
            self.set_new_cell(outsheet, 59, 16, 59, height + index, user_input['building_market_price'][index])
            self.set_new_cell(outsheet, 66, 16, 66, height + index, user_input['building_market_exclusive'][index])
            self.set_new_cell(outsheet, 72, 16, 72, height + index, user_input['building_market_contract'][index])
            self.set_new_cell(outsheet, 78, 16, 78, height + index, user_input['building_market_ma'][index])
            self.set_new_cell(outsheet, 81, 16, 81, height + index, user_input['building_estimated_price'][index])
            self.set_new_cell(outsheet, 88, 16, 88, height + index, user_input['building_estimated_exclusive'][index])
            self.set_new_cell(outsheet, 94, 16, 94, height + index, user_input['building_estimated_contract'][index])
            self.set_new_cell(outsheet, 100, 16, 100, height + index, user_input['building_estimated_ea'][index])
            self.set_new_cell(outsheet, 103, 16, 103, height + index, user_input['building_estimated_em'][index])

        #self.setOutCell(outsheet, 5, 16, user_input['building_ho[]'])

        outbook.save('ibk_output.xls')
        #new_document = Document(file=os.path.join(BASE_DIR, 'output.xls'))
        #new_document.title = 'ibk_output.xls'
        #file = Document.objects.filter(title=new_document.title)
        #if (len(file) == 0):
        #   new_document.save()
        return os.path.join(BASE_DIR, 'ibk_output.xls')