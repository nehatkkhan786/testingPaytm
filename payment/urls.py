from django.urls import path
from .views import *


urlpatterns = [
    path('',HomeView.as_view(),),
    path('initiatepayment/', InitiatePayment.as_view(), name='payment'),
    path('paymentcallback/', PaymentCallbackView.as_view(), ),
]