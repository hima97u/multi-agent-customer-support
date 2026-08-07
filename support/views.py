from django.shortcuts import render
import json

def chat(request,order_id): # comig from order detail sendMessage() fxn
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message")

        print("i/p msg ->" , user_message)