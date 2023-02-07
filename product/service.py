from django_filters import rest_framework as filters
from product.models import Product


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['price']

