from django.urls import path
from tradeadmin import views

urlpatterns = [
    # path('', views.index, name="trade_admin_index"),
    path('traders/', views.trader_list, name="trader_list"),
    path('add-new-trader/', views.add_new_trader, name="new_trader"),
    path('trader_analytics/<str:trader_name>', views.trader_analytics, name="trader_analytics")
]