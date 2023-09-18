from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from data_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path("app/", include("data_app.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
