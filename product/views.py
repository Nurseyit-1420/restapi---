from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import permissions, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CartSerializer, CategorySerializer
from .models import Product, Cart, Category
from users.permissions import IsVendorPermission, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get_context_data(self, id, **kwargs):
        product_id = self.get_object(id=id)
        idiska = product_id.id
        product = Product.objects.get(id=idiska)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'product': product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name
                        },
                    },
                    'quantity': 100,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class CategoryCreateAPIView(APIView):


    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.create(
                name=request.data['name']
            )
            category.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self,request):
        snippets = Category.objects.all()
        serializer = CategorySerializer(snippets, many=True)
        return Response(serializer.data)

class CategoryAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoryFilterAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'id']


class ProductCreateAPIView(APIView):
    # permission_classes = [IsVendorPermission]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                name=request.data['name'],
                vendor_id=request.data['vendor'],
                category_id=request.data['category'],
                description=request.data['description'],
                price=request.data['price']
            )
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAPIListPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


# class ProductListApiView(APIView):
#     permission_classes = [permissions.AllowAny]
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get(self,  request):
#         products = Product.objects.all()
#         paginator = Paginator(products, 3)
#         page_num = self.request.query_params.get('page')
#         serializers = ProductSerializer(paginator.page(page_num), many=True)
#         return Response(serializers.data)
class ProductListAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    pagination_class = ProductAPIListPagination

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'name', 'description', 'id']
    search_fields = ['price', 'name', 'description','id']
    # ?????? ?????????? viewset ?? ???????????????? ???????????? ???????????????????????? ??????????
    # def get(self, request):
    #     snippets = Product.objects.all()
    #     serializer = ProductSerializer(snippets, many=True)
    #     return Response(serializer.data)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        qs = Product.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


class ProductFilterAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['price', 'name', 'id']
    search_fields = ['name', 'description', 'id', 'price']


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        snippet = self.get_object(id)
        serializer = ProductSerializer(snippet)
        return Response(serializer.data)


class ProductUpdateAPIView(APIView):
    permission_classes = [IsVendorPermission, IsOwnerOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, id):
        snippet = self.get_object(id)
        serializer = ProductSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsVendorPermission, IsOwnerOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class AddToCartAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, user_id):
        try:
            return Cart.objects.get(customer_id=user_id)
        except Cart.DoesNotExist:
            raise Http404

    def put(self, request, user_id):
        snippet = self.get_object(user_id)
        serializer = CartSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # pagination_class = CartAPIListPagination
    # authentication_classes = []
    # parser_classes = JSONParser

    def get_object(self, user_id):
        try:
            return Cart.objects.get(customer_id=user_id)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        cart = self.get_object(user_id)
        serializer1 = CartSerializer(cart)
        serializer2 = ProductSerializer(cart.product.all(), many=True)
        data = serializer1.data
        data['product'] = serializer2.data
        return Response(data, status=status.HTTP_200_OK)


