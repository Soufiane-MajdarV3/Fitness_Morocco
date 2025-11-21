from django import forms
from .models import Booking, Review, Payment

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('session_type', 'booking_date', 'start_time', 'duration_minutes', 'notes')
        labels = {
            'session_type': 'نوع الجلسة',
            'booking_date': 'تاريخ الجلسة',
            'start_time': 'وقت البدء',
            'duration_minutes': 'مدة الجلسة',
            'notes': 'ملاحظات إضافية',
        }
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        labels = {
            'rating': 'التقييم',
            'comment': 'تعليقك',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_method',)
        labels = {
            'payment_method': 'طريقة الدفع',
        }
