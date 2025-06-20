from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden('Доступ разрешён только администраторам.')
        # Проверяем роль через профиль
        if not hasattr(user, 'profile') or not user.profile.role or user.profile.role.name != 'Администратор':
            return HttpResponseForbidden('Доступ разрешён только администраторам.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view 