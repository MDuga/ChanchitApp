from django import forms
from core.models import Usuario, Ingresos, Egresos

class RegistroForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirm_password"].label = "Confirma contraseña"

    class Meta:
        model = Usuario
        exclude = ["date_joined"]
        widgets = {
            "password": forms.PasswordInput()
        }
        labels = {
            "usuario": "Nombre de usuario",
            "email": "Correo electrónico",
            "password": "Contraseña"
        }
        error_messages = {
            "usuario": {
                "unique": "nombre de usuario existente",
            },
            "email": {
                "unique": "usuario ya registrado",
            }
        }

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Contraseña incorrecta")
        return self.cleaned_data
    
    def clean_usuario(self):
        usuario = self.cleaned_data.get("usuario")
        if Usuario.objects.filter(usuario=usuario).exists():
            raise forms.ValidationError("Este usuario ya está registrado.")
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    

#========================================================================
class LoginForm(forms.Form):
    
    email = forms.EmailField(label="email")
             
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError("El usuario no está registrado.")

#========================================================================

class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        exclude = ["usuario", "date_registro"]

        labels = {
            "monto": "Monto a ingresar",
            "moneda": "Moneda",
            "descripcion": "Descripción (Ej. mesada)",
            "date_ingreso": "Fecha de entrada (dd/mm/yyyy)"
        }
    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto < 0:
            raise forms.ValidationError("Debes ingresar un número positivo")
        return monto
    
    #========================================================================
class EgresosForm(forms.ModelForm):
    class Meta:
        model = Egresos
        exclude = ["usuario", "date_registro"]

        labels = {
            "monto": "Monto de egreso",
            "moneda": "Moneda",
            "descripcion": "Descripción",
            "date_egreso": "Fecha de egreso (dd/mm/yyyy)"
        }
    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto < 0:
            raise forms.ValidationError("Debes ingresar un número positivo")
        return monto
    
#========================================================================

class QueryMes_Form(forms.Form):
    
    month = forms.IntegerField(min_value=1, max_value=12, label="Mes")
    year = forms.IntegerField(label="Año")

             
#========================================================================
class QueryFechas_Form(forms.Form):
    
    inicio = forms.DateField(label="Inicio")
    fin = forms.DateField(label="Fin")
             
    def clean(self):
        inicio = self.cleaned_data.get("inicio")
        fin = self.cleaned_data.get("fin")
        if inicio and fin and fin < inicio:
            raise forms.ValidationError("La fecha fin debe ser posterior o igual a inicio")
        return self.cleaned_data