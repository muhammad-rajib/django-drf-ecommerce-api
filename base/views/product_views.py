from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from base.models import Product
from base.serializers import ProductSerializer


# Create your views here.
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    # Serialized --> Model Objects to Json
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(reqeust):
    user = reqeust.user

    product = Product.objects.create(
        user            = user,
        name            = 'Sample Name',
        price           = 0,
        brand           = 'Sample brand',
        countInStock    = 0,
        category        = 'Sample Category',
        description     = ''
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser()])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response("Product Deleted")

