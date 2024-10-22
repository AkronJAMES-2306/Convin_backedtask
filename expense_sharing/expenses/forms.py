# expenses/forms.py
from django import forms
from .models import User
from .models import Expense

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'mobile_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise forms.ValidationError("Mobile number must be a 10-digit number.")
        return mobile_number

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'participants']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be a positive number.")
        return amount

    def clean_participants(self):
        participants = self.cleaned_data.get('participants')
        if not participants:
            raise forms.ValidationError("At least one participant is required.")
        return participants

def clean(self):
    cleaned_data = super().clean()
    split_method = cleaned_data.get("split_method")
    percentages = cleaned_data.get("percentages") 

    if split_method == 'percentage' and percentages:
        total_percentage = sum(percentages)
        if total_percentage != 100:
            raise forms.ValidationError("Percentages must add up to 100%.")
