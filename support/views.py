from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
import json
import time
from orders.models import Order
from .models import Conversation
from .models import Message

def chat(request,order_id): # comig from order detail sendMessage() fxn
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message")

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty."}, status=400)

        order = get_object_or_404(Order,id=order_id,user=request.user)

        # this will create a new conversation if it doesn't exist, otherwise it will retrieve the existing one
        conversation,created = Conversation.objects.get_or_create(user=request.user,order=order)

        # storing messages under particular conversation
        Message.objects.create(conversation=conversation,role="user",content=user_message)

        # send user message and converstion to LLM 
        reply = run_support_agent(user_message,conversation.id) # this will return the reply from LLM

        # now we get the reply from user so we will store it as role="agent"
        Message.objects.create(conversation=conversation,role="agent",content=reply)
        time.sleep(6)
        return JsonResponse({"reply":"Here is the reply"})