# core/utils.py
from datetime import date
from core.models import Ingresos, Egresos

def saldo_actual(usuario):
    saldo_actual = 0
    date_actual = date.today()
   
    tipo_movimientos = [
        (Ingresos, 'date_movimiento'),
        (Egresos, 'date_movimiento')
    ]

    for modelo, campo_fecha in tipo_movimientos:
        filtros = {
            'usuario': usuario,
            f"{campo_fecha}__lte": date_actual
        }
        modelos_filtrados_list = modelo.objects.filter(**filtros)
        for i in modelos_filtrados_list:
            saldo_actual += i.monto

    return {
        "usuario": usuario,
        "saldo_actual": saldo_actual,
    }
