from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home_view, AdminDashboardView, ManagerDashboardView, ClientDashboardView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, \
    DeliveryCreateView, DeliveryUpdateView, DeliveryDeleteView, login_view, logout_view, \
    ProductListView, DeliveryListView, OrderListView, DiscountListView, ContactMessageListView, UserListView, ProductDetailView, cart_add, client_profile_view, edit_client_profile_view
from .api_views import ProductViewSet

app_name = 'dobje'

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('manager/dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('client/dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),

    # Product CRUD
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Delivery CRUD
    path('deliveries/create/', DeliveryCreateView.as_view(), name='delivery_create'),
    path('deliveries/<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery_update'),
    path('deliveries/<int:pk>/delete/', DeliveryDeleteView.as_view(), name='delivery_delete'),

    path('login/', login_view, name='login'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('deliveries/', DeliveryListView.as_view(), name='delivery_list'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('discounts/', DiscountListView.as_view(), name='discount_list'),
    path('messages/', ContactMessageListView.as_view(), name='contactmessage_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/add/<int:pk>/', cart_add, name='cart_add'),
    path('profile/', client_profile_view, name='client_profile'),
    path('profile/edit/', edit_client_profile_view, name='edit_client_profile'),
    path('api/', include(router.urls)),
]

