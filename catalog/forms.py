from django import forms
from decimal import Decimal
from .models import Product


class ProductForm(forms.ModelForm):
    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        """Приводим все поля к единой стилистике Bootstrap."""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget

            # Базовый класс стиля
            base_class = 'form-control'

            # Точные соответствия под типы виджетов
            if isinstance(widget, forms.Select):
                base_class = 'form-select'
            elif isinstance(widget, forms.CheckboxInput):
                base_class = 'form-check-input'
            elif isinstance(widget, forms.FileInput):
                base_class = 'form-control'

            # Объединяем существующие классы с базовыми
            existing = widget.attrs.get('class', '').strip()
            widget.attrs['class'] = f"{existing} {base_class}".strip()

        # Дополнительная косметика и доступность
        self.fields['name'].widget.attrs.setdefault('placeholder', 'Введите название товара')
        self.fields['price'].widget.attrs.setdefault('placeholder', '0.00')
        self.fields['description'].widget.attrs.setdefault('rows', 4)

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data['name'].lower()
        self._check_forbidden_words(name, 'названии')
        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get('description', '').lower()
        if description:
            self._check_forbidden_words(description, 'описании')
        return self.cleaned_data['description']

    def _check_forbidden_words(self, text, field_name):
        """Проверка на наличие запрещенных слов"""
        found_words = []
        for word in self.FORBIDDEN_WORDS:
            if word in text:
                found_words.append(word)

        if found_words:
            raise forms.ValidationError(
                f"Обнаружены запрещенные слова в {field_name}: {', '.join(found_words)}"
            )

    def clean_price(self):
        """Кастомная валидация: цена не может быть отрицательной."""
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price < Decimal('0'):
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price