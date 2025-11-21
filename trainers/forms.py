from django import forms
from .models import Trainer, TrainerAvailability, Certificate
from trainers.models import SessionType

class TrainerProfileUpdateForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=SessionType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='التخصصات'
    )
    
    class Meta:
        model = Trainer
        fields = ('specialties', 'experience_years', 'price_per_hour', 'bio')
        labels = {
            'experience_years': 'سنوات الخبرة',
            'price_per_hour': 'السعر بالساعة (درهم)',
            'bio': 'نبذة عنك',
        }


class TrainerAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TrainerAvailability
        fields = ('day_of_week', 'start_time', 'end_time')
        labels = {
            'day_of_week': 'يوم الأسبوع',
            'start_time': 'وقت البدء',
            'end_time': 'وقت الانتهاء',
        }
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('name', 'issuer', 'issue_year', 'document')
        labels = {
            'name': 'اسم الشهادة',
            'issuer': 'جهة الإصدار',
            'issue_year': 'سنة الإصدار',
            'document': 'المستند / الصورة',
        }
