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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    
    user = request.user;

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderPay(request, pk):

    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response("Order was Paid")


# Admin Views
@api_view(["GET"])
@permission_classes([IsAdminUser])
def getOrders(request):

    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):

    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')