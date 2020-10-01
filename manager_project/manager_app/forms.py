from django import forms
from manager_app.models import *



class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        exclude = ('author','payment_type')
        widgets = {
        'title': forms.TextInput(attrs = {'class': 'form-control','placeholder':'Enter Bill No or remakrs'}),
        'date_added': forms.DateInput(attrs = {'class': 'form-control','type':'date'}),
        'final_value': forms.TextInput(attrs = {'class': 'form-control'}),
        'paid_value': forms.TextInput(attrs = {'class': 'form-control'}),
        'is_paid': forms.CheckboxInput(attrs = {'class': 'form-control','type':'checkbox'}),

        'payment_method': forms.Select(attrs = {'class': 'form-control'}),
        # 'payment_type': forms.Select(attrs = {'class': 'form-control'}),
        'payment_update_date': forms.DateInput(attrs = {'class': 'form-control','type':'date'}),
        'bill_category': forms.Select(attrs = {'class': 'form-control'}),
        'firm_name': forms.Select(attrs = {'class': 'form-control'}),
        'benificiary_name': forms.Select(attrs = {'class': 'form-control'}),
                    }





class BenificiaryForm(forms.ModelForm):
    class Meta:
        model = Add_benificiary_name
        exclude = ('balance',)
        widgets = {
        'Benificiary_Name': forms.TextInput(attrs = {'class': 'form-control','placeholder':'Benifiary Name'}),
        'Benificiary_address': forms.TextInput(attrs = {'class': 'form-control'}),
        'Benificiary_AC_number': forms.TextInput(attrs = {'class': 'form-control'}),
        'Benificary_GST_Number': forms.TextInput(attrs = {'class': 'form-control'}),
        'Benificiary_Bank': forms.TextInput(attrs = {'class': 'form-control'}),
        
        'Benificiary_ph_no': forms.TextInput(attrs = {'class': 'form-control'}),
    
                    }

class FirmForm(forms.ModelForm):
    class Meta:
        model = Add_Firm
        fields = "__all__"

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        exclude = ('author','is_paid','payment_type','payment_update_date','title',)
        widgets = {
        'title': forms.TextInput(attrs = {'class': 'form-control','placeholder':'Enter Bill No or remakrs'}),
        'date_added': forms.DateInput(attrs = {'class': 'form-control','type':'date'}),
        'final_value': forms.TextInput(attrs = {'class': 'form-control'}),
        'paid_value': forms.TextInput(attrs = {'class': 'form-control'}),
        'person':forms.Select(attrs={'class':'form-control'}),

        'payment_method': forms.Select(attrs = {'class': 'form-control'}),
        # 'payment_type': forms.Select(attrs = {'class': 'form-control'}),
        'firm_name':forms.Select(attrs = {'class': 'form-control'}),
        
        
                    }

class GenericExpenseForm(forms.ModelForm):
    class Meta:
        model = GenericExpense
        exclude = ('author','payment_type','payment_update_date','is_paid','paid_value')
        widgets = {
        'title': forms.TextInput(attrs = {'class': 'form-control','placeholder':'Enter Expense Name'}),
        'date_added': forms.DateInput(attrs = {'class': 'form-control','type':'date'}),
        'final_value': forms.TextInput(attrs = {'class': 'form-control'}),
        # 'paid_value': forms.TextInput(attrs = {'class': 'form-control'}),
        # 'is_paid': forms.CheckboxInput(attrs = {'class': 'form-control','type':'checkbox'}),

        'payment_method': forms.Select(attrs = {'class': 'form-control'}),
        # 'payment_type': forms.Select(attrs = {'class': 'form-control'}),
        # 'payment_update_date': forms.DateInput(attrs = {'class': 'form-control','type':'date'}),
        'category': forms.Select(attrs = {'class': 'form-control'}),
        'firm_name':forms.Select(attrs = {'class': 'form-control'}),}
    
