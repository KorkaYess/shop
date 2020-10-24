from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Category, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    subs = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subs']


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=False
    )
    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'products']


class ProductSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.ReadOnlyField(source='subcategory.name')
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all(), write_only=False
    )
    category_name = serializers.ReadOnlyField(
        source='subcategory.category.name'
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'description',
            'subcategory', 'category_name', 'subcategory_name'
        ]
