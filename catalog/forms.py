import re
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Перераховуємо поля, які клієнт МАЄ заповнити сам
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                  'country', 'city', 'postal_code', 'address']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        
        # 1. Дозволяємо лише цифри, пробіли, тире та плюс на початку
        # Регулярний вираз: ^\+?[\d\s\-]{9,}$
        # Це означає: може бути +, далі цифри, пробіли або тире, мінімум 9 символів
        if not re.match(r'^\+?[\d\s\-]{9,}$', phone):
            raise forms.ValidationError("Invalid format. Use digits, spaces, '-' or '+' (min 9 digits).")
        
        # 2. Додаткова перевірка: скільки ПЕРЕБУВАЄ саме цифр (без плюсів і тире)
        only_digits = re.sub(r'\D', '', phone) # Видаляємо ВСЕ, що не є цифрою
        if len(only_digits) < 9:
            raise forms.ValidationError("The phone number must contain at least 9 digits.")
            
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code').strip()
        
        # Перевірка: тільки цифри і довжина 5-6
        if not postal_code.isdigit():
            raise forms.ValidationError("Postal code must contain only digits.")
        
        if not (3 <= len(postal_code) <= 6):
            raise forms.ValidationError("Postal code must be 3 or 6 digits.")
            
        return postal_code

class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(
        required=False, 
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Min'})
        )
    max_price = forms.DecimalField(
        required=False, 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Min'})
        )

    def clean(self):
        cleaned_data = super().clean()
        min_p = cleaned_data.get('min_price')
        max_p = cleaned_data.get('max_price')

        if min_p and max_p:
            if min_p > max_p:
                self.add_error('max_price', 'Ensure this value is greater than min value.')
                pass
        return cleaned_data

   