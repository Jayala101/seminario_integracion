"""
Piede salario y clasidica el cargo 
<1000 junior
1000-2000 semi senior
>2000 senior
"""

salario = int(input("Salario es:"))

if salario < 1000:
    cargo = "junior"
elif salario >=1000 & salario <=2000:
    cargo = "semi senior"
else:
    cargo = "senior"

print(f"El cargo es: {cargo}")


