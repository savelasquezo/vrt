from django.urls import path, include
from .views import HomeView, InterfaceView, TicketFormView, HistoryListView, InvestmentView


urlpatterns = [

    path("accounts/", include("django.contrib.auth.urls")),
    path('', HomeView.as_view(), name='Home'),
    path('investment', InvestmentView.as_view(), name='Investment'),
    path('accounts/profile/', InterfaceView.as_view(), name='Interface'),
    path('accounts/profile/ticket/', TicketFormView.as_view(), name='Tickets'),
    path('accounts/profile/history', HistoryListView.as_view(), name='History'),
]


