from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .products import products  

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    return Response('Hello')

@api_view(['GET'])
def getProducts(request):
    return Response(products)

@api_view(['GET'])
def getProduct(request, pk):
    product = None
    for item in products:
        if item['_id'] == pk:
            product = item
            break
    return Response(product)
    