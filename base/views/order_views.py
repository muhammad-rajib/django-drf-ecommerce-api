from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'details': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # Create Order
        order = Order.objects.create(
            user            = user,
            paymentMethod   = data['paymentMethod'],
            taxPrice        = data['taxPrice'],
            shippingPrice   = data['shippingPrice'],
            totalPrice      = data['totalPrice']
        )

        # Create shipping address
        shipping = ShippingAddress.objects.create(
            order       = order,
            address    = data['shippingAddress']['address'],
            city        = data['shippingAddress']['city'],
            postalCode  = data['shippingAddress']['postalCode'],
            country     = data['shippingAddress']['country']
        )

        # Create Order Items
        for itm in orderItems:
            product = Product.objects.get(_id=itm['product'])

            item = OrderItem.objects.create(
                product = product,
                order   = order,
                name    = product.name,
                qty     = itm['qty'],
                price   = itm['price'],
                image   = product.image.url,
            )

            # update stock
            product.countInStock -= item.qty
            product.save()
        
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
