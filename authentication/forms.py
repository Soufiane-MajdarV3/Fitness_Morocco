from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='تأكيد كلمة المرور')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'city', 'user_type')
        labels = {
            'username': 'اسم المستخدم',
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'city': 'المدينة',
            'user_type': 'نوع الحساب',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError('كلمات المرور غير متطابقة')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label='اسم المستخدم أو البريد الإلكتروني')
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'city', 'profile_image', 'bio')
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'city': 'المدينة',
            'profile_image': 'صورة الملف الشخصي',
            'bio': 'نبذة عنك',
        }
