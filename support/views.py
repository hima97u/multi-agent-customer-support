from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
import json
import time
from orders.models import Order
from support.agents import run_support_agent
from support.models import Message
from django.contrib.admin.views.decorators import staff_member_required
from .models import Conversation
from .langchain_agents import run_support_agent_langchain
from .event_queue import publish, subscribe, unsubscribe


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

        # publish user message event so that connected clients can receive it
        event = {
            "type": "user_message",
            "message": user_message,
            "name": request.user.first_name
        }
        publish(conversation.id, event)

        # send user message and converstion to LLM
        reply = run_support_agent_langchain(user_message,conversation.id,order.id,request.user.id) # this will return the reply from LLM ### => langchain done

        # # print("REPLY:", repr(reply)) for debugging purposes
        # # print("REPLY TYPE:", type(reply))

        # now we get the reply from user so we will store it as role="agent"
        Message.objects.create(conversation=conversation,role="agent",content=reply)


        # time.sleep(6) # now no need of sleep because we are not using streaming response, we are sending the reply after getting it from LLM so no need of sleep
        return JsonResponse({"reply":reply})


@staff_member_required
def dashboard(request):
    conversations = Conversation.objects.all().order_by("-created_at")
    print('conversations===>', conversations)
    context = {
        'conversations': conversations,
    }
    return render(request, "support/dashboard.html", context)


@staff_member_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by("created_at")
    agentlogs = conversation.agentlogs.order_by("created_at")

    context = {
        "conversation": conversation,
        "messages": messages,
        "agentlogs": agentlogs
    }
    return render(request, "support/conversation_detail.html", context)


# @staff_member_required
def conversation_stream(request, conversation_id):
    def event_stream(conversation_id):
        q = subscribe(conversation_id)

        try:
            while True:
                event = q.get() # wait for the next event

                yield f"data: {json.dumps(event)}\n\n"
        finally:
            unsubscribe(conversation_id, q)

    response = StreamingHttpResponse(
        event_stream(conversation_id),
        content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response