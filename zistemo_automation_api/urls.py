from django.contrib import admin
from django.urls import path
from zistemo_automation_api.views import reportes
from zistemo_automation_api.views import catalogos

urlpatterns = [
    # Django default admin
        path('admin/', admin.site.urls),
    # Construcción de catálogos
        path('catalogos/proyectos', catalogos.CatalogoProyectosView.as_view()),
    # Reportes
        path('reporte/', reportes.DescargarReporteView.as_view())
]
