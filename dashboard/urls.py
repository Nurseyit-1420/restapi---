from django.urls import path
from . import views
from dashboard.views import VendorListAPIView, CustomerListAPIView, UserListView, CategoryListApiView, LenProduct, PriceApiView



urlpatterns = [
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('vendors/', views.dashboard_with_pivot_vendors, name='dashboard_with_pivot_vendors'),
    path('customers/', views.dashboard_with_pivot_customers, name='dashboard_with_pivot_customers'),
    path('data/', views.pivot_data, name='pivot_data'),
    path('data_vendor/', views.pivot_data_vendor, name='pivot_data_vendor'),
    path('data_customer/', views.pivot_data_customer, name='pivot_data_customer'),
    path('cat/list/', CategoryListApiView.as_view(), name='cat-list'),
    path('statistic/', PriceApiView.as_view(), name='statistic'),
    path('len_product/', LenProduct.as_view(), name='products'),
]



"""----------------------------------"""
# from django.urls import path
#
# from dashboard.views import VendorListAPIView, CustomerListAPIView, UserListView, CategoryListApiView, LenProduct, \
#     PriceApiView
#
# urlpatterns = [
#     path('vendor/list/', VendorListAPIView.as_view(), name='vendor-list'),
#     path('customer/list/', CustomerListAPIView.as_view(), name='customer-list'),
#     path('user/list/', UserListView.as_view(), name='user-list'),
#     path('cat/list/', CategoryListApiView.as_view(), name='cat-list'),
#     path('statistic/', PriceApiView.as_view(), name='statistic'),
#     path('len_product/', LenProduct.as_view(), name='products'),
# ]