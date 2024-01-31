from django import forms

class SearchPdfForm(forms.Form):
    keywords = forms.CharField(max_length=255)
    pdf_file = forms.FileField()

