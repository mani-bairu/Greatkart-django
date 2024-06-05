from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'   
    }))
    confirn_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirn Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email Address'
       
       

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        total_clear_data=super().clean()
        password=total_clear_data['password']
        confirm_password=total_clear_data['confirn_password']
        if password != confirm_password:
            raise forms.ValidationError("password missmatch!!")