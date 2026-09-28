from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('account/create/',AccountCreateView.as_view(),name='account'),
    path('account/detail/',AccountDetailView.as_view(),name='account_detail'),
    
    path('cards/',CardListView.as_view(),name='cards'),
    path('card/create/',CardCreateView.as_view(),name='card_create'),
    path('card/<int:pk>/',CardDetailView.as_view(),name='card_detail'),

    path('transfer/',TransferView.as_view(),name='transfer'),
    path('history/',HistoryView.as_view(),name='history'),
    path('card-history/',CardHistoryView.as_view(),name='card_history'),
    path('check-phone/',CheckPhoneView.as_view(),name='check_phone'),
    path('check-card/',CheckCardView.as_view(),name='check_card')
]