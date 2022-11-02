from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import logging

from .models import BankStatement, DepositRequest, WithdrawalRequest


def index(request):
    return render(request, "search_data.html")


# Create your views here.
def uploadstatement(request):
    readSuccess = False
    audit_type = ""
    if "GET" == request.method:
        return render(request, 'uploadstatement.html')
    else:
        data_check = request.POST 
        audit_types = ["WithDrawal Requests", "Deposit Requests"]
        if data_check.get('fileType') == "2":
            messages.error(request, "Please Select Audit Type")
            return HttpResponseRedirect(reverse("uploadstatement"))
        
        try:
            auditFile = request.FILES["auditFile"]
            bankstatement = request.FILES["bankstatement"]
            if not auditFile.name.endswith('.csv') and not bankstatement.name.endswith('.csv'):
                messages.error(request,'Please provide both files in csv format')
                return HttpResponseRedirect(reverse("uploadstatement"))

            audit_type = audit_types[int(data_check.get("fileType"))]

            auditFileData = auditFile.read().decode("utf-8")
            bankFileData = bankstatement.read().decode("utf-8")
            auditFilelines = auditFileData.split("\n")
            bankFilelines = bankFileData.split("\n")
            auditDataDict = []
            bankDataDict = []
            auditHeaders = auditFilelines[0].split(",")
            bankHeaders = bankFilelines[0].split(",")

            for i in range(1, len(auditFilelines)-1):						
                auditFields = auditFilelines[i].split(",")
                collectionData = {}
                for index, head in enumerate(auditHeaders):
                    collectionData.update({
                        head: auditFields[index],
                    })
                auditDataDict.append(collectionData)

            # Bank statement
            for i in range(1, len(bankFilelines)-1):						
                bankFields = bankFilelines[i].split(",")
                collectionData = {}
                for index, head in enumerate(bankHeaders):
                    collectionData.update({
                        head: bankFields[index],
                    })
                bankDataDict.append(collectionData)
            
            readSuccess = True
            contents = {
                'status': readSuccess,
                'audit_type': audit_type,
                'auditHeaders': auditHeaders,
                'auditDataDict': auditDataDict,
                'bankHeaders': bankHeaders,
                'bankDataDict': bankDataDict,
            }
            return render(request, 'uploadstatement.html', contents)
        except Exception as ex:
            print("========================ERROR=========================")
            print(ex)
            messages.error(request, str(ex)+', please check columns must be in this format: name, amount')
            return HttpResponseRedirect(reverse("uploadstatement"))


suditTypes = ["Withdrawal Requests", "Deposit Requests"]

def search(request):
    if "GET" == request.method:
        return render(request, "search_data.html")

    print('=================================================')
    print(request.POST)
    print('=================================================')


    searchFields = request.POST
    audit_date = searchFields.get('searchDate')
    auditType = searchFields.get("fileType")
    auditObj = WithdrawalRequest if not auditType else DepositRequest
    
    if int(auditType) == 2:
        messages.warning(request, "Please select audit type")        
        return HttpResponseRedirect(reverse("search"))

    auditData = auditObj.objects.filter(audit_date=audit_date)
    bankStatementData, auditRequestData = match(request.POST)
    # finalResult = {}
    # auditStatement = []
    # bankStatement = []
    # for audit in auditData:
    #     amount = audit.amount
    #     name = audit.customer
    #     number_of_names = str(name).split(" ")
        
    #     obj = BankStatement.objects.filter(amount=amount, audit_date=audit_date)
        
        
    #     for nms in number_of_names:
    #         obj = obj.filter(customer__icontains=nms)

    #     if obj.count() > 0:
    #         bankst = obj.first()
    #         bankStatement.append({
    #             "ID": bankst.user_id, 
    #             "amount": bankst.amount, 
    #             "customar": bankst.customer, 
    #             "request_date": bankst.date, 
    #             "audit_date": bankst.audit_date
    #         })
            
    #     else:
    #         bankStatement.append({
    #             "ID": "N/A", 
    #             "amount": "N/A", 
    #             "customar": "N/A", 
    #             "request_date": "N/A", 
    #             "date": "N/A"
    #         })
    #     auditStatement.append({
    #         "ID": audit.user_id, 
    #         "amount": audit.amount, 
    #         "customar": audit.customer, 
    #         "request_date": audit.date, 
    #         "audit_date": audit.audit_date
    #     })
    #     finalResult.update({
    #         "bankSatement": bankStatement,
    #         "auditSatement": auditStatement
    #     })
    
    # print('=====================================')
    # print(finalResult)
    # print('=====================================')
    
    contenxt = {
        "bankStatementData": bankStatementData,
        "auditRequestData": auditRequestData,
        "audit_date": audit_date,
        "auditType": auditType,
        "auditTypeHeading": suditTypes[int(auditType)]
    }
    return render(request, "search_data.html", contenxt)



def filter_by_amount(item,  class_object_name, filter_columns):
    ...

def filter_by_date(item,  class_object_name, filter_columns):
    filtered_data = class_object_name.objects.filter(amount__gte=(item.amount-3.0),amount__lte=(item.amount+3.0), audit_date=item.audit_date)
    statuses = ["not matched", "parcialy matched", "fully matched", "only amount matched", "amount with single name matched"] 
    colors = ["red", "yellow", "green", "lightblue", "amount with single name matched"] 
    status = statuses[0]
    color = colors[0]
    matched_id = 0
    splitted_names = str(item.customer).split(" ")

    for i, nms in enumerate(splitted_names):
        obj = filtered_data.filter(customer__icontains=nms)
        if obj:
            trueIndex +=1
            if trueIndex >=1:
                status = statuses[trueIndex]
                matched_id = obj.first().user_id
        else:
            if trueIndex > 0:
                trueIndex -=1
            if trueIndex > -1:
                status = statuses[trueIndex]
                color = colors[trueIndex]
        if i == len(splitted_names)-1 and (filtered_data.filter(amount=item.amount).count() == 1 and status == "not matched"):
            status = "Only Amount Matched"
            color = "lightblue"

        return matched_id, status, trueIndex


def formatData(item,  class_object_name, filter_columns=None):    
    filtered_data = class_object_name.objects.filter(amount__gte=(item.amount-3.0),amount__lte=(item.amount+3.0), audit_date=item.audit_date)

    statuses = ["not matched", "parcialy matched", "fully matched", "only amount matched"] 
    status = statuses[0]
    colors = ["#fb7c7c", "#dbdb49", "#9cf576", "lightblue"] 
    color = colors[0]
    matched_id = 0
    trueIndex = 0
    splitted_names = str(item.customer).split(" ")

    for i, nms in enumerate(splitted_names):
        obj = filtered_data.filter(customer__icontains=nms)
        if obj:
            trueIndex +=1
            if trueIndex >=1:
                status = statuses[trueIndex]
                color = colors[trueIndex]
                matched_id = obj.first().user_id
        else:
            if trueIndex > 0:
                trueIndex -=1
            if trueIndex > -1:
                status = statuses[trueIndex]
                color = colors[trueIndex]
        if i == len(splitted_names)-1 and (filtered_data.filter(amount=item.amount).count() == 1 and status == "not matched"):
            status = "Only Amount Matched"
            color = "lightblue"

    return  {
                "ID": item.user_id, 
                "amount": item.amount, 
                "customar": item.customer, 
                "request_date": item.date, 
                "audit_date": item.audit_date,
                "matched_id":matched_id, 
                "status":status,
                'color': color
            }

            


def match(obj):    
    auditType = obj.get("fileType")
    audit_date = obj.get("searchDate")
    auditObj = WithdrawalRequest if auditType == '0' else DepositRequest

    auditFilterWithDate = auditObj.objects.filter(audit_date=audit_date)
    bankFilterWithDate = BankStatement.objects.filter(audit_date=audit_date)

    bankStatementData = list(map(lambda x: formatData(x, auditObj, obj.get('columns')) ,bankFilterWithDate)) 
    auditRequestData = list(map(lambda x: formatData(x, BankStatement, obj.get('columns')),auditFilterWithDate)) 
    
    return bankStatementData, auditRequestData
    

