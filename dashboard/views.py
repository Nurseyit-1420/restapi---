from django.http import JsonResponse
from django.shortcuts import render
from dashboard.models import Order
from django.core import serializers
from product.models import Product, Cart, Category
from product.serializers import CartSerializer
from users.models import Customer, Vendor, MyUser
"""" -----------------------------------------------  """
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Category, Product
from product.serializers import CategorySerializer
from users.models import Vendor, Customer, MyUser
from users.serializer import VendorSerializer, CustomerSerializer

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})
def dashboard_with_pivot_vendors(request):
    return render(request, 'dashboard_vendor.html', {})
def dashboard_with_pivot_customers(request):
    return render(request, 'dashboard_customer.html', {})
def pivot_data(request):
    dataset = Product.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
def pivot_data_vendor(request):
    dataset = Vendor.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
def pivot_data_customer(request):
    dataset = Customer.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


"""" -----------------------------------------------  """








# Create your views here.



class VendorListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def get(self, request):
        snippets = Vendor.objects.all()
        serializer = VendorSerializer(snippets, many=True)
        return Response(serializer.data)



class CustomerListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    # authentication_classes = []

    def get(self, request):
        snippets = Customer.objects.all()
        serializer = CustomerSerializer(snippets, many=True)
        return Response(serializer.data)


class CategoryListApiView(APIView):

    # def get(self, request):
    #     category = Category.objects.all()
    #     serializers = CategorySerializer(category, many=True)
    #     return Response(serializers.data)
    def get(self, request):
        category = Category.objects.all()
        posts = []
        for i in category:
            posts.append(i.id)

        category = len(posts)

        data = {
            "category": category
        }
        return Response(data)

class UserListView(APIView):

    def get(self, request):
        users = MyUser.objects.all()
        user_list = []
        for i in users:
            user_list.append(i.username)

        username = len(user_list)

        data = {
            "users": username,
        }
        return Response(data)

class PriceApiView(APIView):

    def get(self, request):
        products = Product.objects.all()
        price_list = []
        for i in products:
            price_list.append(i.price)
        max_price = max(price_list)
        min_price = min(price_list)
        avg_price = sum(price_list) / len(price_list)

        data = {
            "max_price": max_price,
            "min_price": min_price,
            "avg_price": avg_price,
        }
        return Response(data)

class LenProduct(APIView):

    def get(self, request):
        products = Product.objects.all()
        posts = []
        for i in products:
            posts.append(i.id)

        product = len(posts)

        data = {
            "product": product
        }
        return Response(data)

