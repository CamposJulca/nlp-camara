from django.contrib import admin
from django.urls import path, include
from camara_app.views import ExtraerCertificadosApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('camara_app.urls')),
    path('api/extraer/', ExtraerCertificadosApiView.as_view(), name='api-extraer'),
]
