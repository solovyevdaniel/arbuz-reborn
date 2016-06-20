from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=70)
    file = forms.FileField()
