from django import forms
from django.utils import timezone
from agenda.models import Evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = ["usuario", "moneda", "date_creacion", "date_cierre"]

        labels = {
            "titulo": "Nombre del evento",
            "date_evento": "Fecha del evento (dd/mm/yyyy)",
            "monto": "Monto deseado",        
            "tipo_evento": "Tipo de evento",
            "estado": "Estado"
            }
    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto < 0:
            raise forms.ValidationError("Debes ingresar un número positivo")
        return monto
    
    
    def clean_date_evento(self):
        fecha = self.cleaned_data.get("date_evento")
        if fecha and fecha < timezone.now().date():
            raise forms.ValidationError("La fecha no puede ser anterior a hoy.")
        return fecha
    

#====================================================================================