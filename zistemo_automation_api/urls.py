from django.contrib import admin
from django.urls import path
from zistemo_automation_api.views import reportes
from zistemo_automation_api.views import catalogos

urlpatterns = [
    # Django default admin
        path('admin/', admin.site.urls),
    # Construcción de catálogos
        path('catalogos/proyectos', catalogos.CatalogoProyectosView.as_view()),
        path('catalogos/usuarios', catalogos.CatalogoUsuariosView.as_view()),
    # Reportes
        path('timesheet/', reportes.TimesheetSaveView.as_view()),
        path('reporte/', reportes.CrearReporteDiaView.as_view())
]
