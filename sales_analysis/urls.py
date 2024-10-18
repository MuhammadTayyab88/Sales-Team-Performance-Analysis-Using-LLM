# sales_analysis/urls.py

from django.urls import path
from .views import individual_performance_view, team_performance_view,performance_trends_view,rep_performance_view,performance_dashboard
from . import views
urlpatterns = [
    path('', performance_dashboard, name='performance_dashboard'),
    path('api/individual_performance/<int:employee_id>/', individual_performance_view, name='individual_performance'),
    path('api/team_performance/<str:team_name>/', views.team_performance_view, name='team_performance'),
    path('api/rep_performance/<int:rep_id>/', rep_performance_view, name='rep_performance'),
    path('api/performance_trends/', performance_trends_view, name='performance_trends'),
]
