from django import forms
from .models import Producto, ConsultaCliente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Asegúrate de colocar solo los campos que existen en ferreteria/models.py
        fields = ['nombre', 'precio', 'stock', 'categoria', 'imagen'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }


class ConsultaClienteForm(forms.ModelForm):
    class Meta:
        model = ConsultaCliente
        fields = ['nombre', 'correo', 'mensaje', 'producto_interes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'producto_interes': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje')
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe contener al menos 10 caracteres.")
        return mensaje