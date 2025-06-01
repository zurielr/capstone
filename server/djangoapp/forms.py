from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["car", "review", "purchase", "purchase_date"]


class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, label="Review")
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Purchase Date")
    car_make = forms.CharField(label="Car Make")
    car_model = forms.CharField(label="Car Model")
    car_year = forms.IntegerField(label="Car Year", min_value=2015, max_value=2023)

