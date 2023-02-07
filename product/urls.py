from django.urls import path
from .views import (
    ProductCreateAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    AddToCartAPIView,
    CartDetailAPIView,
    ProductFilterAPIView,
    ProductListAPIView,
    CategoryCreateAPIView,
    CategoryListAPIView,
    CategoryFilterAPIView,

)

urlpatterns = [
    path('list/', ProductListAPIView.as_view(), name='product-list'),
    path('filter/', ProductFilterAPIView.as_view(), name='product-filter'),
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('<int:id>/detail/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('<int:id>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:id>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),

    path('add_to_cart/<int:user_id>/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart_detail/<int:user_id>/', CartDetailAPIView.as_view(), name='cart-detail'),

    path('category/create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('category/list/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/filter/', CategoryFilterAPIView.as_view(), name='category-filter'),
]


