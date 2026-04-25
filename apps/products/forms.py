from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'url', 'marketplace', 'category', 'status',
            'notify_whatsapp', 'notify_telegram', 'notify_promotion',
            'price_target', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/produto'
            }),
            'marketplace': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Categoria do produto'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price_target': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição detalhada do produto'
            }),
            'notify_whatsapp': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notify_telegram': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notify_promotion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            # Validação básica de URL
            if not (url.startswith('http://') or url.startswith('https://')):
                raise forms.ValidationError('A URL deve começar com http:// ou https://')
        return url

    def clean_price_target(self):
        price_target = self.cleaned_data.get('price_target')
        if price_target is not None and price_target <= 0:
            raise forms.ValidationError('O preço alvo deve ser maior que zero.')
        return price_target

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
                if hasattr(field.widget, 'attrs'):
                    if 'placeholder' in field.widget.attrs:
                        field.widget.attrs['placeholder'] += ' *'
