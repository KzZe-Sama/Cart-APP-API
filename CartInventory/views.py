from django.db.models import query
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.permissions import OR, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import ItemSerializer,OrderSerializer,CategorySerializer,CartSerializer,OrderItemSerializer
from .models import Item,Category,OrderItem,Order,CartItem
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ItemViews(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    permission_classes = (AllowAny,) 
    serializer_class = ItemSerializer

    def list(self,request):
        querySet = self.get_queryset()
        serializer = ItemSerializer(querySet,many=True)
        return Response(serializer.data)

class OrderViews(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        querySet = Order.objects.filter(user_id=request.user).order_by("-id")
        serializer = OrderSerializer(querySet,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class OrderItemView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def list(self, request,order_id,*args, **kwargs):
        querySet = OrderItem.objects.filter(order_id=order_id)
        serializer = OrderItemSerializer(querySet,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AllUserOrderItemView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def list(self, request,*args, **kwargs):
        querySet = OrderItem.objects.filter(user_id=request.user)
        serializer = OrderItemSerializer(querySet,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class OrderItemUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self, order_id):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return Order.objects.get(id=order_id)
        except OrderItem.DoesNotExist:
            raise Http404
    def patch(self, request, order_id, format=None):
        item_order = self.get_object(order_id= order_id)
        serializer = OrderSerializer(item_order,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         

   

class CategoryViews(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self,request,cat_id=None):
        # print("args",cat_id)
        if cat_id != None :
            querySet = Category.objects.filter(id=cat_id)
            serializer = CategorySerializer(querySet,many=True)
            return Response(serializer.data)
        else:
            querySet = self.get_queryset()
            serializer = CategorySerializer(querySet,many=True)
            return Response(serializer.data)

class CartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, user_id):
        querySet = CartItem.objects.filter(user=user_id,ordered=False)
        serializer = CartSerializer(querySet,many=True)
        return Response(serializer.data)

class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, cart_id):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return CartItem.objects.get(id=cart_id)
        except CartItem.DoesNotExist:
            raise Http404
    def patch(self, request, cart_id, format=None):
        cart = self.get_object(cart_id=cart_id)
        serializer = CartSerializer(cart,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

   

class CartDeleteItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, user_id,cart_id):
        instance = CartItem.objects.filter(user=user_id,id=cart_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
     