from django import forms

from orders import models


class OrderForm(forms.ModelForm):
    email = forms.CharField(max_length=255)

    class Meta:
        model = models.Order
        fields = ('robot_serial',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
