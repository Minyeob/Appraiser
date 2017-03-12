from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import *
from estimation.models import Bookmark
#  파일을 import 할 때 from 에서 .을 이용하면 파일경로를 전부 칠 필요없이 현재 파일이 속한 파일의 다른 파일들을 가져올 수 있다
from .forms import UploadFileForm
from .models import Document
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from .functiom import *
import xlrd
from django import shortcuts
from django.core.files import File
import os


# Create your views here.

class Bookmark_ListView(ListView):
    model = Bookmark

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
            normals=zip(normal_datas, normal_codes)
            file=Document.objects.filter(title=new_document.title)
            #해당파일이 이미 존재하면 저장하지 않고 해당파일이 없다면 해당 파일의 데이터 모델을 저장한다
            if(len(file)==0):
                new_document.save()

            return render(request,'estimation/code_selection.html', {'normals':normals, 'file':new_document})

    else:
        form=UploadFileForm()
    documents = Document.objects.all()


    return render(request,'estimation/upload_file.html',{'documents':documents, 'form':form})

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
    ho=excel_handling().get_ho(workbook, code)  #건물의 호들
    liensize_improvement=excel_handling().get_liensize_improvement(workbook, code)  #전유면적 - 일단 엑셀에서 건물면적을 꺼내서 구함
    landsize=excel_handling().get_landsize(workbook, code)  #대지권 면적
    utensil=excel_handling().get_utensil(workbook, loc) #기계기구의 숫자

    address_code=excel_handling().get_address_code(workbook,loc)


    return render(request, 'estimation/normal_report.html',
                  {'code':code,'borrow_name':borrow_name, 'program':program_title, 'property_control_no':property_control_no, 'court':court, 'case':case, 'opb':opb,
                   'interest':interest, 'setup_price':setup_price, 'address':address, 'category':category, 'ho':ho,
                   'liensize_improvement':liensize_improvement, 'landsize':landsize, 'utensil':utensil, 'address_code':address_code})
