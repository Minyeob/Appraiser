from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='업로드하실 엑셀파일을 선택해주세요')

class ExcelForm(forms.Form):

    #결과요약

    program=forms.CharField(required=False) #program
    opb=forms.CharField(required=False) #opb
    interest=forms.CharField(required=False)    #연체이자
    property_control_no=forms.CharField(required=False) #property_no
    setup_price=forms.CharField(required=False) #설정액
    user=forms.CharField(required=False)    #담당자
    user_phone=forms.CharField(required=False)  #담당자 연락처
    credit_amount=forms.CharField(required=False)   #총 채권액
    borrow_name=forms.CharField(required=False) #borrow name
    law_price=forms.CharField(required=False)   #법사가
    market_predict=forms.CharField(required=False)  #시장전망
    market_price=forms.CharField(required=False)    #시장가
    law_price_comp1=forms.CharField(required=False) #법사가 대비 1
    market_price_comp1=forms.CharField(required=False)  #시장가 대비 1
    opb_comp1=forms.CharField(required=False)   #opb 대비 1
    court=forms.CharField(required=False)   #관할법원
    bid=forms.CharField(required=False) #낙찰가
    law_price_comp2 = forms.CharField(required=False)   #법사가 대비 2
    market_price_comp2 = forms.CharField(required=False)    #시장가 대비 2
    opb_comp2 = forms.CharField(required=False) #opb 대비 2
    case=forms.CharField(required=False)    #사건번호
    avg_bid=forms.CharField(required=False) #평균낙찰가
    law_price_comp3 = forms.CharField(required=False)  # 법사가 대비 3
    market_price_comp3 = forms.CharField(required=False)  # 시장가 대비 3
    opb_comp3 = forms.CharField(required=False)  # opb 대비 3
    submission_date = forms.CharField(required=False)   #법원제출일
    next_date = forms.CharField(required=False) #차기기일
    fail_count = forms.CharField(required=False) #유찰회수

    #본건현황


    #건물
    ho=forms.CharField(required=False)


