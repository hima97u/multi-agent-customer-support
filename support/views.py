from django.http import JsonResponse
from django.shortcuts import render
import json
import time

def chat(request,order_id): # comig from order detail sendMessage() fxn
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message")

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty."}, status=400)

        time.sleep(6)
        return JsonResponse({"reply":"Here is the reply"})