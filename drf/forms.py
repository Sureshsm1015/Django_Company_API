from django import forms
from .models import company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = ['name', 'location', 'about', 'type','added_Date', 'active']


from .models import employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = employee
        fields = ['name', 'email', 'address', 'phone_no','join_date', 'position', 'salary', 'company']
