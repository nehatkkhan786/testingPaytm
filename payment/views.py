from django.shortcuts import render
from django.views import View
import paytmchecksum 
import requests
import json
from django.http import HttpResponse

import uuid

def generate_order_id():
    return str(uuid.uuid4())

# Create your views here.

PAYTM_MERCHANT_ID = 'DIY12386817555501617'
PAYTM_SECRET_KEY = 'bKMfNxPPf_QdZppa' 

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Homepage.html' )
    

class InitiatePayment(View):
    def post(self, request, *args, **kwargs):
        paytmParams = dict()
        paytmParams['body'] = {
            "requestType"   : "Payment",
            "mid"           : PAYTM_MERCHANT_ID,
            "websiteName"   : "Vecreation",
            "orderId"       : generate_order_id(),
            "callbackUrl"   : "https://<callback URL to be used by merchant>",
            "txnAmount"     : {
                "value"     : "1.00",
                "currency"  : "INR",
            },
            "userInfo"      : {
                "custId"    : "CUST_001",
            },
        }
        checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_SECRET_KEY)
        paytmParams["head"] = {
            "signature" : checksum
        }
        post_data = json.dumps(paytmParams)
        # for Staging
        url = f'https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MERCHANT_ID}&orderId={paytmParams["body"]["orderId"]}'

        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        result = {
            "txToken" : response["body"]["txnToken"],
            "orderId": paytmParams['body']['orderId'],
            "amount": paytmParams["body"]["txnAmount"]["value"]

        }
        print(response["body"]["txnToken"])
        return render(request, "paymentrequest.html", {"result":result})







class PaymentCallbackView(View):
    def get(self, request, *args, **kwargs):
        pass