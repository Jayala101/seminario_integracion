"""
Pide le numero de empleados y luego el sueldo de cada uno 
suma y muestar la nomina total
"""

empleados = int(input("Numero de empleados:"))
nomina = 0

for i in range(empleados):
    sueldo = float(input(f"Sueldo empleado {i+1}:"))
    nomina += sueldo

print(f"La nómina total es: {nomina}")