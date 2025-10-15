"""
Sistema que pida pago por hora y horas trabajadas
Las primeras 40h son normales, las extreas se pagan el 150%
Calcula y muestra el pago total
"""
pago_hora = float(input("El pago por hora: "))
horas = float(input("Horas trabajadas: "))
if horas <= 40:
    pago_total = horas * pago_hora
else:
    horas_extra = horas - 40
    pago_total = (40 * pago_hora) + (horas_extra * pago_hora * 1.5)
print(f"Pago total: {pago_total:.2f}")
