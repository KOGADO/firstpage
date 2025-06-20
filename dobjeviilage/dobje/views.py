from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Role, City, User, Address, Category, Product, Cart, CartItem, Favorite, Order, OrderItem, Review, Discount, Delivery, ProductIngredient, ContactMessage, UserProfile
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .forms import LoginForm, ClientProfileForm, ClientProfileExtraForm
from django.views.decorators.http import require_POST
from random import sample
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'dobje/home.html')

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Редирект по роли
                if hasattr(user, 'profile') and hasattr(user.profile, 'role') and user.profile.role and user.profile.role.name == 'Менеджер':
                    return redirect('dobje:manager_dashboard')
                elif hasattr(user, 'profile') and hasattr(user.profile, 'role') and user.profile.role and user.profile.role.name == 'Админ':
                    return redirect('dobje:admin_dashboard')
                else:
                    return redirect('dobje:client_dashboard')
            else:
                error = "Неверное имя пользователя или пароль"
    else:
        form = LoginForm()
    return render(request, 'dobje/login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('dobje:login')

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile') or not user.profile.role:
            return False
        return user.profile.role.name in self.allowed_roles
    def handle_no_permission(self):
        raise PermissionDenied("У вас нет доступа к этой странице.")

class RoleListView(RoleRequiredMixin, ListView):
    model = Role
    template_name = 'dobje/role_list.html'
    context_object_name = 'roles'
    allowed_roles = ['Администратор']

class RoleDetailView(DetailView):
    model = Role
    template_name = 'dobje/role_detail.html'
    context_object_name = 'role'

class CityListView(ListView):
    model = City
    template_name = 'dobje/city_list.html'
    context_object_name = 'cities'

class CityDetailView(DetailView):
    model = City
    template_name = 'dobje/city_detail.html'
    context_object_name = 'city'

class UserListView(RoleRequiredMixin, ListView):
    model = User
    template_name = 'dobje/user_list.html'
    context_object_name = 'users'
    allowed_roles = ['Администратор']

class UserDetailView(RoleRequiredMixin, DetailView):
    model = User
    template_name = 'dobje/user_detail.html'
    context_object_name = 'user'
    allowed_roles = ['Администратор']

class AddressListView(ListView):
    model = Address
    template_name = 'dobje/address_list.html'
    context_object_name = 'addresses'

class AddressDetailView(DetailView):
    model = Address
    template_name = 'dobje/address_detail.html'
    context_object_name = 'address'

class CategoryListView(RoleRequiredMixin, ListView):
    model = Category
    template_name = 'dobje/category_list.html'
    context_object_name = 'categories'
    allowed_roles = ['Администратор', 'Менеджер']

class CategoryDetailView(RoleRequiredMixin, DetailView):
    model = Category
    template_name = 'dobje/category_detail.html'
    context_object_name = 'category'
    allowed_roles = ['Администратор', 'Менеджер']

class ProductListView(RoleRequiredMixin, ListView):
    model = Product
    template_name = 'dobje/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Показывать 10 продуктов на странице
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']

class ProductDetailView(RoleRequiredMixin, DetailView):
    model = Product
    template_name = 'dobje/product_detail.html'
    context_object_name = 'product'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']

class CartListView(RoleRequiredMixin, ListView):
    model = Cart
    template_name = 'dobje/cart_list.html'
    context_object_name = 'carts'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент':
            return qs.filter(user=user)
        return qs

class CartDetailView(RoleRequiredMixin, DetailView):
    model = Cart
    template_name = 'dobje/cart_detail.html'
    context_object_name = 'cart'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент' and obj.user != user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return obj

class CartItemListView(RoleRequiredMixin, ListView):
    model = CartItem
    template_name = 'dobje/cartitem_list.html'
    context_object_name = 'cartitems'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент':
            return qs.filter(cart__user=user)
        return qs

class CartItemDetailView(RoleRequiredMixin, DetailView):
    model = CartItem
    template_name = 'dobje/cartitem_detail.html'
    context_object_name = 'cartitem'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент' and obj.cart.user != user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return obj

class FavoriteListView(RoleRequiredMixin, ListView):
    model = Favorite
    template_name = 'dobje/favorite_list.html'
    context_object_name = 'favorites'
    allowed_roles = ['Администратор', 'Клиент']
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент':
            return qs.filter(user=user)
        return qs

class FavoriteDetailView(RoleRequiredMixin, DetailView):
    model = Favorite
    template_name = 'dobje/favorite_detail.html'
    context_object_name = 'favorite'
    allowed_roles = ['Администратор', 'Клиент']
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент' and obj.user != user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return obj

class OrderListView(RoleRequiredMixin, ListView):
    model = Order
    template_name = 'dobje/order_list.html'
    context_object_name = 'orders'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент':
            return qs.filter(user=user)
        return qs

class OrderDetailView(RoleRequiredMixin, DetailView):
    model = Order
    template_name = 'dobje/order_detail.html'
    context_object_name = 'order'
    allowed_roles = ['Администратор', 'Менеджер', 'Клиент']
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент' and obj.user != user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return obj

class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'dobje/orderitem_list.html'
    context_object_name = 'orderitems'

class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = 'dobje/orderitem_detail.html'
    context_object_name = 'orderitem'

class ReviewListView(RoleRequiredMixin, ListView):
    model = Review
    template_name = 'dobje/review_list.html'
    context_object_name = 'reviews'
    allowed_roles = ['Администратор', 'Клиент']
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент':
            return qs.filter(user=user)
        return qs

class ReviewDetailView(RoleRequiredMixin, DetailView):
    model = Review
    template_name = 'dobje/review_detail.html'
    context_object_name = 'review'
    allowed_roles = ['Администратор', 'Клиент']
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if hasattr(user, 'role') and user.role and user.role.name == 'Клиент' and obj.user != user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return obj

class DiscountListView(RoleRequiredMixin, ListView):
    model = Discount
    template_name = 'dobje/discount_list.html'
    context_object_name = 'discounts'
    allowed_roles = ['Администратор', 'Менеджер']

class DiscountDetailView(RoleRequiredMixin, DetailView):
    model = Discount
    template_name = 'dobje/discount_detail.html'
    context_object_name = 'discount'
    allowed_roles = ['Администратор', 'Менеджер']

class DeliveryListView(RoleRequiredMixin, ListView):
    model = Delivery
    template_name = 'dobje/delivery_list.html'
    context_object_name = 'deliveries'
    allowed_roles = ['Администратор', 'Менеджер']

class DeliveryDetailView(RoleRequiredMixin, DetailView):
    model = Delivery
    template_name = 'dobje/delivery_detail.html'
    context_object_name = 'delivery'
    allowed_roles = ['Администратор', 'Менеджер']

class ProductIngredientListView(RoleRequiredMixin, ListView):
    model = ProductIngredient
    template_name = 'dobje/productingredient_list.html'
    context_object_name = 'productingredients'
    allowed_roles = ['Администратор', 'Менеджер']

class ProductIngredientDetailView(RoleRequiredMixin, DetailView):
    model = ProductIngredient
    template_name = 'dobje/productingredient_detail.html'
    context_object_name = 'productingredient'
    allowed_roles = ['Администратор', 'Менеджер']

class ContactMessageListView(RoleRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'dobje/contactmessage_list.html'
    context_object_name = 'contactmessages'
    allowed_roles = ['Администратор', 'Менеджер']

class ContactMessageDetailView(RoleRequiredMixin, DetailView):
    model = ContactMessage
    template_name = 'dobje/contactmessage_detail.html'
    context_object_name = 'contactmessage'
    allowed_roles = ['Администратор', 'Менеджер']

class AdminDashboardView(TemplateView):
    template_name = 'dobje/admin_dashboard.html'

class ManagerDashboardView(TemplateView):
    template_name = 'dobje/manager_dashboard.html'

class ClientDashboardView(TemplateView):
    template_name = 'dobje/client_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = list(Product.objects.exclude(image=''))
        if len(products) >= 3:
            context['popular_products'] = sample(products, 3)
        else:
            context['popular_products'] = products
        return context

class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    template_name = 'dobje/product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dobje:product_list')
    allowed_roles = ['Администратор', 'Менеджер']

class ProductUpdateView(RoleRequiredMixin, UpdateView):
    model = Product
    template_name = 'dobje/product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dobje:product_list')
    allowed_roles = ['Администратор', 'Менеджер']

class ProductDeleteView(RoleRequiredMixin, DeleteView):
    model = Product
    template_name = 'dobje/product_confirm_delete.html'
    success_url = reverse_lazy('dobje:product_list')
    allowed_roles = ['Администратор', 'Менеджер']

class DeliveryCreateView(RoleRequiredMixin, CreateView):
    model = Delivery
    template_name = 'dobje/delivery_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dobje:delivery_list')
    allowed_roles = ['Администратор', 'Менеджер']

class DeliveryUpdateView(RoleRequiredMixin, UpdateView):
    model = Delivery
    template_name = 'dobje/delivery_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dobje:delivery_list')
    allowed_roles = ['Администратор', 'Менеджер']

class DeliveryDeleteView(RoleRequiredMixin, DeleteView):
    model = Delivery
    template_name = 'dobje/delivery_confirm_delete.html'
    success_url = reverse_lazy('dobje:delivery_list')
    allowed_roles = ['Администратор', 'Менеджер']

@require_POST
def cart_add(request, pk):
    from django.shortcuts import get_object_or_404
    from django.contrib.auth import get_user_model
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    User = get_user_model()
    if not user.is_authenticated or not hasattr(user, 'profile') or user.profile.role.name != 'Клиент' or not isinstance(user, User):
        return redirect('dobje:login')
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('dobje:cartitem_list')

@login_required
def client_profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    addresses = user.addresses.all() if hasattr(user, 'addresses') else []
    return render(request, 'dobje/client_profile.html', {
        'user': user,
        'profile': profile,
        'addresses': addresses,
    })

@login_required
def edit_client_profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        user_form = ClientProfileForm(request.POST, instance=user)
        profile_form = ClientProfileExtraForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('dobje:client_profile')
    else:
        user_form = ClientProfileForm(instance=user)
        profile_form = ClientProfileExtraForm(instance=profile)
    return render(request, 'dobje/edit_client_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })