from django.shortcuts import render

# Create your views here.
from apps.uploadstatement.models import DepositRequest, WithdrawalRequest
from django.views.generic import CreateView, UpdateView

class DepositRequestCreateView(CreateView):
    model = DepositRequest
    fields = "__all__"


class DepositRequestUpdateView(UpdateView):
    model = DepositRequest
    fields = "__all__"

def DepositRequestDeleteView(request, pk):
    obj = DepositRequest.objects.get(pk=pk)
    obj.delete()
    return obj.get_absolute_url()


class WithdrawalRequestCreateView(CreateView):
    model = WithdrawalRequest
    fields = "__all__"

class WithdrawalRequestUpdateView(UpdateView):
    model = WithdrawalRequest
    fields = "__all__"

def WithdrawalRequestDeleteView(request, pk):
    obj = WithdrawalRequest.objects.get(pk=pk)
    obj.delete()
    return obj.get_absolute_url()

