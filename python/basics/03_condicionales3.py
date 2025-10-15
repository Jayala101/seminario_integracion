"""
Vcaciones por antiguedad
pide años de antiguedad y muestra dias de vacaciones segun
<1=0
<3=3
<5=10
>=5=15
"""

años_antiguedad = int(input("Años de antiguedad es:"))

if años_antiguedad < 1:
    dias_vacaciones = 0
elif años_antiguedad < 3:
    dias_vacaciones = 3
elif años_antiguedad < 5:
    dias_vacaciones = 10
else:
    dias_vacaciones = 15

print(f"Dias de vacaciones son: {dias_vacaciones}")