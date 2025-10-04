from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": None,
            "password1": None,
            "password2": None
        }
        error_messages = {
            "username": {"unique": "Ese usuario ya existe, probá con otro 😅"},
            "email": {"unique": "Este correo ya está registrado 🚨"}
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nombre de usuario"
        self.fields["email"].label = "Correo electrónico"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Ups! Las contraseñas no coinciden 🥺")
        return password2
    

#========================================================================

class LoginForm(forms.Form):

    email = forms.EmailField(
        label="Correo electrónico"
        )
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput
        )
    
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        usuario = authenticate(username = email, password = password)
        if usuario is None:            
            raise forms.ValidationError("Usuario o contraseña incorrecto.")
        
        self.user = usuario
        return self.cleaned_data
        
#========================================================================

class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "avatar", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"})
        }