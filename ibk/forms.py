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

    address=forms.CharField(required=False) #Address
    property_category=forms.CharField(required=False)   #Property category
    usage=forms.CharField(required=False)   #용도지역
    land_category=forms.CharField(required=False)   #지목
    state=forms.CharField(required=False)   #이용상황
    land_price_m=forms.CharField(required=False)    #개별공시지가 m
    land_price_py=forms.CharField(required=False)   #개별공시지가 py
    land_size_m=forms.CharField(required=False) #전체토지면적 m
    land_size_py=forms.CharField(required=False)   #전체토지면적 py
    security_size_m=forms.CharField(required=False) #담보면적 m
    security_size_py=forms.CharField(required=False)    #담보면적 py
    structure=forms.CharField(required=False)   #건물 구조
    permission_date=forms.CharField(required=False) #사용승인일
    floor_usage=forms.CharField(required=False) #층별 용도
    exclusive_rate=forms.CharField(required=False)  #전용율
    exclusive_area_m=forms.CharField(required=False)    #전유면적 m
    exclusive_area_py=forms.CharField(required=False)   #전유면적 py
    contract_area_m=forms.CharField(required=False) #계약면적 m
    contract_area_py=forms.CharField(required=False)    #계약면적 py

    #건물

    building_label=forms.CharField(required=False)
    building_ho=forms.CharField(required=False)
    building_exclusive_m=forms.CharField(required=False)
    building_exclusive_py=forms.CharField(required=False)
    bulding_contract_m=forms.CharField(required=False)
    building_contract_py=forms.CharField(required=False)
    building_right_m=forms.CharField(required=False)
    building_right_py=forms.CharField(required=False)
    building_ratio=forms.CharField(required=False)
    building_auction_price=forms.CharField(required=False)
    building_auction_exclusive=forms.CharField(required=False)
    building_auction_contract=forms.CharField(required=False)
    building_auction_ratio=forms.CharField(required=False)
    building_market_price = forms.CharField(required=False)
    building_market_exclusive = forms.CharField(required=False)
    building_market_contract = forms.CharField(required=False)
    bulding_market_ma=forms.CharField(required=False)
    building_estimated_price = forms.CharField(required=False)
    building_estimated_exclusive = forms.CharField(required=False)
    building_estimated_contract = forms.CharField(required=False)
    bulding_estimated_ea = forms.CharField(required=False)
    bulding_estimated_em = forms.CharField(required=False)



