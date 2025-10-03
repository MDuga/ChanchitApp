from django import forms
from core.models import Ingresos, Egresos

class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        exclude = ["usuario", "date_registro"]

        labels = {
            "monto": "Monto a ingresar",
            "moneda": "Moneda",
            "descripcion": "Descripción (Ej. mesada)",
            "date_movimiento": "Fecha de entrada (dd/mm/yyyy)"
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
            "date_movimiento": "Fecha de egreso (dd/mm/yyyy)"
        }
    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto < 0:
            raise forms.ValidationError("Debes ingresar un número positivo")
        return monto
    
#========================================================================
class QueryMes_Form(forms.Form):
    
    month = forms.IntegerField(min_value=1, max_value=12, label="Mes")
    year = forms.IntegerField(min_value=2000, label="Año")
    
                 
#========================================================================
# Para hacer búsqueda por rango de echa
class QueryFechas_Form(forms.Form):
    
    inicio = forms.DateField(
        label="Inicio",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    
    fin = forms.DateField(
        label="Fin", 
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
             
    def clean(self):
        inicio = self.cleaned_data.get("inicio")
        fin = self.cleaned_data.get("fin")
        if inicio and fin and fin < inicio:
            raise forms.ValidationError("La fecha fin debe ser posterior o igual a inicio")
        return self.cleaned_data