from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def area_triangulo(request):
    try:
        base = float(request.data.get('base',0))
        altura = float(request.data.get('altura',0))
    except (TypeError, ValueError):
        return Response({"error": "Parámetros inválidos"}, status=status.HTTP_400_BAD_REQUEST)
    area = (base * altura) / 2
    return Response({
        "base": base,
        "altura": altura,
        "area": area
    })

@api_view(['GET'])
def tabla_multiplicar(request):
    try:
        # read from query params for GET requests
        numero = float(request.query_params.get('numero', 0))
    except (TypeError, ValueError):
        return Response({"error": "número inválido"}, status=status.HTTP_400_BAD_REQUEST)
    tabla = [f"{numero}x{i} = {numero*i}" for i in range(1,13)]
    return Response({
        "numero": numero,
        "tabla": tabla,
    })


@api_view(['POST'])
def contar_mayores(request):
    try:
        numeros = request.data.get('numeros',[])
        limite = request.data.get('limite',[])
    except (TypeError, ValueError):
        return Response({'error': "Paramtros invalidos"},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        limite = float(limite)
        lista_numeros = [float(n) for n in numeros]
    except (TypeError, ValueError):
        return Response({"error": "valores numericos inválidos"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    contador = 0
    for n in lista_numeros:
        if n > limite:
            contador += 1
    return Response({
        "numeros": lista_numeros,
        "limite": limite,
        "mayores": contador
    })


@api_view(['POST'])
def suma_descendente(request):
    try:
        n_raw = request.data.get('n', None)
        if n_raw is None:
            return Response({"error": "Falta el parámetro 'n'"}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError):
        return Response({"error": "Parámetros inválidos"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        n = int(n_raw)
    except (TypeError, ValueError):
        return Response({"error": "'n' debe ser un entero"}, status=status.HTTP_400_BAD_REQUEST)
    if n < 1:
        return Response({"error": "'n' debe ser >= 1"}, status=status.HTTP_400_BAD_REQUEST)
    secuencia = [i for i in range(n, 0, -1)]
    suma = sum(secuencia)
    return Response({
        "n": n,
        "secuencia": secuencia,
        "suma": suma
    })


@api_view(['POST'])
def promedio_lista(request):
    try:
        numeros = request.data.get('numeros', None)
        if numeros is None:
            return Response({"error": "Falta el parámetro 'numeros'"}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError):
        return Response({"error": "Parámetros inválidos"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        lista = [float(x) for x in numeros]
    except Exception:
        return Response({"error": "La lista debe contener solo números"}, status=status.HTTP_400_BAD_REQUEST)
    cantidad = len(lista)
    if cantidad == 0:
        return Response({"error": "La lista 'numeros' no puede estar vacía"}, status=status.HTTP_400_BAD_REQUEST)
    promedio = sum(lista) / cantidad
    return Response({
        "numeros": lista,
        "cantidad": cantidad,
        "promedio": promedio
    })

