from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='업로드하실 엑셀파일을 선택해주세요'
    )

