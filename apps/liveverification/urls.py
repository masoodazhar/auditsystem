from django.urls import path, include
from .views import (
    DepositRequestCreateView,
    DepositRequestUpdateView,
    DepositRequestDeleteView
)


app_name = "liveverification"
urlpatterns = [
    path('', DepositRequestCreateView.as_view(template_name="liveverification/DepositRequestCreateView.html"), name="DepositRequestCreateView"),
    path('<int:pk>/Edit', DepositRequestUpdateView.as_view(template_name="liveverification/DepositRequestUpdateView.html"), name="DepositRequestUpdateView"),
    path('<int:pk>/Delete', DepositRequestDeleteView, name="DepositRequestDeleteView"),
]
