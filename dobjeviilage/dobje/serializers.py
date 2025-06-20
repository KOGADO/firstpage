from rest_framework import serializers
from .models import Product, Category

class ProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления продуктов."""
    # Принимаем ID категории
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

class ProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения продуктов."""
    # Показываем имя категории
    category = serializers.StringRelatedField()
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image'] 