from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home_page"),
    path("", views.home, name="home"),
    # path('temp-table/', views.show_temp_table, name='temp_table'),
    path('get_employee_details/', views.get_employee_details, name='get_employee_details'), 
    path("reports/", views.reports, name="reports"),
    path('generate_report/', views.generate_report, name='generate_report'),
    path("view_report/", views.view_report, name="view_report"),
    path("download_pdf/", views.download_pdf, name="download_pdf"),
]
