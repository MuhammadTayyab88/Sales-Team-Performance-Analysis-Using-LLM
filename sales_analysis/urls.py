# sales_analysis/urls.py

from django.urls import path
from .views import (
    individual_performance_view, 
    team_performance_view,
    performance_trends_view, 
    performance_dashboard
)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Main dashboard
    path('', performance_dashboard, name='performance_dashboard'),

    # Individual performance based on employee_name (string)
    path('api/individual_performance/<str:employee_name>/', individual_performance_view, name='individual_performance'),

    # Team performance - team_name passed as a query parameter
    path('api/team_performance/', team_performance_view, name='team_performance'),

    # Monthly performance trends (time period via query params)
    path('api/performance_trends/', performance_trends_view, name='performance_trends'),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
