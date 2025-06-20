from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Role, City, User, Address, Category, Product, Cart, CartItem, Favorite,
    OrderStatus, Order, OrderItem, Discount, DeliveryStatus, Delivery, Review,
    ContactMessage, ProductIngredient, UserProfile
)

User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)
admin.site.register(DeliveryStatus)
admin.site.register(Delivery)
admin.site.register(Review)
admin.site.register(ContactMessage)
admin.site.register(ProductIngredient)
