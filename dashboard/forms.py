from django import forms
from .models import Users,Application


class RegForm(forms.ModelForm):
    CHOICES = [
        ('S', 'Student'),
        ('F', 'Faculty'),
    ]
    role = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'tb'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))

    class Meta:
        model = Users
       
        fields=['first_name','last_name','email','password','role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'tb'}),
            'last_name': forms.TextInput(attrs={'class': 'tb'}),
            'email': forms.TextInput(attrs={'class': 'tb'}),
            
        }


class loginForm(forms.Form):
    user_id=forms.CharField(widget=forms.TextInput(attrs={'class': 'tb'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))

class ApplicationForm(forms.ModelForm):
    CHOICES = [
        ('Online', 'Online'),
        ('On Campus', 'On-Campus'),
    ]
    study_mode=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect(attrs={'class': 'tb'}), required=True)
    class Meta:
        model = Application
       
        fields=['uni_name','prog_name','study_mode']
        widgets = {
            'uni_name': forms.TextInput(attrs={'class': 'tb'}),
            'prog_name': forms.TextInput(attrs={'class': 'tb'}),    
        }
        labels = {
            'uni_name': 'University Name',
            'prog_name': 'Program Name',
            'study_mode' : 'Study Mode'
        }


class ChangePassForm(forms.Form):
    current_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))
    new_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))