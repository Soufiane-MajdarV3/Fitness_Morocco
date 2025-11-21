from django import forms
from .models import ClientProfile

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ('age', 'gender', 'fitness_level', 'goals', 'weight', 'height')
        labels = {
            'age': 'العمر',
            'gender': 'الجنس',
            'fitness_level': 'مستوى اللياقة',
            'goals': 'أهدافك الصحية',
            'weight': 'الوزن (كجم)',
            'height': 'الطول (سم)',
        }
