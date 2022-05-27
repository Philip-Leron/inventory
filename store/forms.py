from django import forms
from .models import Product,Brand,Category


class ProdutForm(forms.ModelForm):
    class Meta:
        model=Product
        serial=forms.CharField(label='Serial')
        fields=['brand','category','serial','image']

class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        brand=forms.CharField(label='Brand')
        fields=['brand']
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        category=forms.CharField(label='Category')
        fields=['category']
'''
class ReceiverForm(forms.Form):
    receivers=forms.MultipleChoiceField(queryset=Receiver.objects.raw('SELECT name FROM store_Receiver'))
    '''