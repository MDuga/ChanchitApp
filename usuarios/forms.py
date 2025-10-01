from django import forms
from usuarios.models import Usuario

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
