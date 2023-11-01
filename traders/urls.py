from django.urls import path
from traders import views

urlpatterns = [
    path('login/', views.login, name="trader_login"),
    path('dashboard/<str:trader_name>', views.trader_dashboard, name="trader_dashboard")
]

