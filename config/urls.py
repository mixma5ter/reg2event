from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('events/admin/', admin.site.urls),
    path('events/auth/', include('users.urls', namespace='users')),
    path('events/auth/', include('django.contrib.auth.urls')),
    path('events/forms/', include('forms.urls', namespace='forms')),
    path('events/reg/', include('reg.urls', namespace='reg')),
]

# Обработчики страниц ошибок
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'
