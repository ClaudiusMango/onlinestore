from django import forms
from .models import CheckOutInfo

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOutInfo
        exclude = ['order']

class ProductSearchForm(forms.Form):
    category_name = forms.CharField(required=True)
    product_name = forms.CharField(required=True)