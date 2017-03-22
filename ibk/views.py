from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import *
#  파일을 import 할 때 from 에서 .을 이용하면 파일경로를 전부 칠 필요없이 현재 파일이 속한 파일의 다른 파일들을 가져올 수 있다
from .forms import UploadFileForm, ExcelForm
from .models import Document
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from .function import *
import xlrd
from django import shortcuts
from django.core.files import File
import os
import urllib.request
import xmltodict

#get으로 해당 페이지에 접속하면 파일을 업로드할 수 있는 폼을 제공, 파일을 업로드해서 업로드버튼을 누르면 해당 파일에 있는 데이터로 각 사건에 대해 보기를 제공
def upload_file(request):
    if request.method == 'POST':
        form=UploadFileForm(request.POST, request.FILES)

        #자신이 만든 폼의 필드는 기본값으로 required=true 로 되어 있으므로 모든 필드가 입력되지 않으면 유효하지 않다
        if form.is_valid():
            new_document=Document(file=request.FILES['file'])
            new_document.title=new_document.file.name
            workbook =excel_handling().make_file(new_document.file)
            normal_datas=excel_handling().get_normal(workbook)
            normal_codes=excel_handling().get_normal_code(workbook)
            normal_zip=zip(normal_datas, normal_codes)
            file=Document.objects.filter(title=new_document.title)
            animal = ['cat', 'dog', 'mause']
            how_many = ['one', 'two', 'three']
            data = zip(animal, how_many)

            #해당파일이 이미 존재하면 저장하지 않고 해당파일이 없다면 해당 파일의 데이터 모델을 저장한다
            if(len(file)==0):
                new_document.save()

            return render(request,'ibk/templatemo_497_upper/templatemo_497_upper/code_selection.html', {'normals':normal_zip, 'file':new_document, 'codes':data})

    else:
        form=UploadFileForm()

    return render(request,'ibk/templatemo_497_upper/templatemo_497_upper/form.html',{'form':form})

#탁감 보고서를 작성하기 위해 엑셀데이터에서 필요한 데이터를 추출해서 html 페이지로 데이터를 보내준다
def show_normal_report(request, code):
    name=request.GET['title']
    file=Document.objects.get(title=name)
    loc=0;
    workbook = excel_handling().make_file(file.file)
    #모든 데이터로 데이터 집합을 구해 보통 같은 행의 데이터는 하나의 대상에 대한 곧통의 데이터를 가르키므로 해당 행의 위치를 구해 나머지도 구한다
    codes = excel_handling().get_all_code(workbook)
    while(loc<len(codes)):
        if(codes[loc]==code):
            break
        else:
            loc=loc+1
    borrow_name=excel_handling().get_render_name(workbook, loc)    #Borrow Name
    program_title=excel_handling().get_program_title(workbook)  #Program
    property_control_no=excel_handling().get_property_control_no(workbook,loc) #Property Control No
    court=excel_handling().get_court(workbook,loc)  #관할법원
    case=excel_handling().get_case_number(workbook, loc)    #사건번호
    borrower_num=excel_handling().get_render_index(workbook, loc)   #차주일련번호
    opb=excel_handling().get_opb(workbook, borrower_num)    #OPB
    interest=excel_handling().get_accured_interest(workbook, borrower_num)  #연체이자
    setup_price=excel_handling().get_cpma(workbook, loc) #설정액
    address=excel_handling().get_address(workbook, loc, code)    #Address
    category=excel_handling().get_property_category(workbook, loc)  #Property category
    label=['가','나','다','라','마','바','사','아','자','차','카','타','파','하']
    ho=excel_handling().get_ho(workbook, code)  #건물의 호들
    liensize_improvement=excel_handling().get_liensize_improvement(workbook, code)  #전유면적 - 일단 엑셀에서 건물면적을 꺼내서 구함
    landsize=excel_handling().get_landsize(workbook, code)  #대지권 면적
    building=zip(label, ho, liensize_improvement, landsize)
    utensil=excel_handling().get_utensil(workbook, loc) #기계기구의 숫자

    address_code=excel_handling().get_address_code(workbook,loc)

    #url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcSHRent?LAWD_CD=11110&DEAL_YMD=201702&serviceKey=KqP4dQTZbN2QbXZlZUK0gYsfRfqiACwnmgqPf3N2yPqj%2F7Ura0eDpY1CKVPmzzQRqGS3myGv3Oauhw7YmfPDLg%3D%3D'
    #data = urllib.request.urlopen(url).read()
    #sample=xmltodict.parse(data)['response']['body']['items']['item'][1]['계약면적']

    #download_url=excel_write().save_file(program_title, opb, property_control_no, interest, setup_price)

    return render(request, 'ibk/report.html',
                  {'code':code,'borrow_name':borrow_name, 'program':program_title, 'property_control_no':property_control_no, 'court':court, 'case':case, 'opb':opb,
                   'interest':interest, 'setup_price':setup_price, 'address':address, 'category':category, 'building':building, 'utensil':utensil,
                   'address_code':address_code})

def download(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST)
        #form은 valid 검사를 하고 나서야 cleaned_data를 가진다
        if form.is_valid():
            #dictionary 형태로 선언하기 위해서는 중괄호 {} 로 선언해야 한다
            user_input={}
            #결과요약
            user_input['program'] = form.cleaned_data['program']
            user_input['opb'] = form.cleaned_data['opb']
            user_input['interest'] = form.cleaned_data['interest']
            user_input['property_control_no'] = form.cleaned_data['property_control_no']
            user_input['setup_price'] = form.cleaned_data['setup_price']
            user_input['user'] = form.cleaned_data['user']
            user_input['user_phone'] = form.cleaned_data['user_phone']  # 담당자 연락처
            user_input['credit_amount'] = form.cleaned_data['credit_amount'] # 총 채권액
            user_input['borrow_name'] = form.cleaned_data['borrow_name']  # borrow name
            user_input['law_price'] = form.cleaned_data['law_price']  # 법사가
            user_input['market_predict'] = form.cleaned_data['market_predict']  # 시장전망
            user_input['market_price'] = form.cleaned_data['market_price']  # 시장가
            user_input['law_price_comp1'] = form.cleaned_data['law_price_comp1']  # 법사가 대비 1
            user_input['market_price_comp1'] = form.cleaned_data['market_price_comp1']    # 시장가 대비 1
            user_input['opb_comp1'] = form.cleaned_data['opb_comp1']  # opb 대비 1
            user_input['court'] = form.cleaned_data['court']  # 관할법원
            user_input['bid'] = form.cleaned_data['bid']  # 낙찰가
            user_input['law_price_comp2'] = form.cleaned_data['law_price_comp2']  # 법사가 대비 2
            user_input['market_price_comp2'] = form.cleaned_data['market_price_comp2']  # 시장가 대비 2
            user_input['opb_comp2'] = form.cleaned_data['opb_comp2']  # opb 대비 2
            user_input['case'] = form.cleaned_data['case']  # 사건번호
            user_input['avg_bid'] = form.cleaned_data['avg_bid']  # 평균낙찰가
            user_input['law_price_comp3'] = form.cleaned_data['law_price_comp3']  # 법사가 대비 3
            user_input['market_price_comp3'] = form.cleaned_data['market_price_comp3']  # 시장가 대비 3
            user_input['opb_comp3'] = form.cleaned_data['opb_comp3']  # opb 대비 3
            user_input['submission_date'] = form.cleaned_data['submission_date']  # 법원제출일
            user_input['next_date'] = form.cleaned_data['next_date']  # 차기기일
            user_input['fail_count'] = form.cleaned_data['fail_count']  # 유찰회수

            #본건현황
            user_input['address'] = form.cleaned_data['address']  # Address
            user_input['property_category'] = form.cleaned_data['property_category']  # Property category
            user_input['usage'] = form.cleaned_data['usage']  # 용도지역
            user_input['land_category'] = form.cleaned_data['land_category']  # 지목
            user_input['state'] = form.cleaned_data['state']  # 이용상황
            user_input['land_price_m'] = form.cleaned_data['land_price_m']  # 개별공시지가 m
            user_input['land_price_py'] = form.cleaned_data['land_price_py']  # 개별공시지가 py
            user_input['land_size_m'] = form.cleaned_data['land_size_m']  # 전체토지면적 m
            user_input['land_size_py'] = form.cleaned_data['land_size_py']  # 전체토지면적 py
            user_input['security_size_m'] = form.cleaned_data['security_size_m']  # 담보면적 m
            user_input['security_size_py'] = form.cleaned_data['security_size_py']  # 담보면적 py
            user_input['structure'] = form.cleaned_data['structure']  # 건물 구조
            user_input['permission_date'] = form.cleaned_data['permission_date']  # 사용승인일
            user_input['floor_usage'] = form.cleaned_data['floor_usage']  # 층별 용도
            user_input['exclusive_rate'] = form.cleaned_data['exclusive_rate']  # 전용율
            user_input['exclusive_area_m'] = form.cleaned_data['exclusive_area_m']  # 전유면적 m
            user_input['exclusive_area_py'] = form.cleaned_data['exclusive_area_py']  # 전유면적 py
            user_input['contract_area_m'] = form.cleaned_data['contract_area_m']  # 계약면적 m
            user_input['contract_area_py'] = form.cleaned_data['contract_area_py']  # 계약면적 py

            #건물
            user_input['building_label']=request.POST.getlist('building_label[]')
            user_input['building_ho'] = request.POST.getlist('building_ho[]')
            user_input['building_exclusive_m']=request.POST.getlist('building_exclusive_m[]')
            user_input['building_exclusive_py'] = request.POST.getlist('building_exclusive_py[]')
            user_input['building_contract_m'] = request.POST.getlist('building_contract_m[]')
            user_input['building_contract_py'] = request.POST.getlist('building_contract_py[]')
            user_input['building_right_m'] = request.POST.getlist('building_right_m[]')
            user_input['building_right_py'] = request.POST.getlist('building_right_py[]')
            user_input['building_ratio'] = request.POST.getlist('building_ratio[]')
            user_input['building_auction_price'] = request.POST.getlist('building_auction_price[]')
            user_input['building_auction_exclusive'] = request.POST.getlist('building_auction_exclusive[]')
            user_input['building_auction_contract'] = request.POST.getlist('building_auction_contract[]')
            user_input['building_auction_ratio'] = request.POST.getlist('building_auction_ratio[]')
            user_input['building_market_price'] = request.POST.getlist('building_market_price[]')
            user_input['building_market_exclusive'] = request.POST.getlist('building_market_exclusive[]')
            user_input['building_market_contract'] = request.POST.getlist('building_market_contract[]')
            user_input['building_market_ma'] = request.POST.getlist('building_market_ma[]')
            user_input['building_estimated_price'] = request.POST.getlist('building_estimated_price[]')
            user_input['building_estimated_exclusive'] = request.POST.getlist('building_estimated_exclusive[]')
            user_input['building_estimated_contract'] = request.POST.getlist('building_estimated_contract[]')
            user_input['building_estimated_ea'] = request.POST.getlist('building_estimated_ea[]')
            user_input['building_estimated_em'] = request.POST.getlist('building_estimated_em[]')

            print(user_input['building_estimated_price'])

            excel_write().save_file(user_input)

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            #MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            file_path=os.path.join(BASE_DIR, 'ibk_output.xls')
            fh=open(file_path, 'rb')
            response=HttpResponse(fh.read(), content_type='application/vnd.ms-excel')
            # 파일이름은 한글로 되어있으면 다운로드를 제공할때 올바르게 제공되지 않는다 - 이유확인해보기
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
