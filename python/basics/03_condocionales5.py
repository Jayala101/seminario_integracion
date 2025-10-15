"""
pide salario y desempeño (1-5)
si el desempeño es:
>4=15%
>3=10%
>2=5%
>1=2%
"""

salario = float(input("Ingrese el salario: "))
desempeno = int(input("Ingrese el desempeño (1-5): "))

if (desempeno > 4):
    calculo = salario * 1.5
elif (desempeno > 3):
    calculo = salario * 1
elif (desempeno > 2):
    calculo = salario * 0.5
elif (desempeno > 1):
    calculo = salario * 0.2
else: 
    calculo = salario

print(f"Total: {calculo}")