from django.shortcuts import render, get_object_or_404
from .models import Order, RefundRequest
from django.contrib.auth.decorators import login_required
from support.models import Conversation


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'orders_list.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # get refund history for this order
    refunds = RefundRequest.objects.filter(order=order)

    # This is to show previous messages in the conversation related to this order, if any.
    try:
        conversation = Conversation.objects.get(user=request.user, order=order)
        previous_messages = conversation.messages.order_by("created_at")
    except Conversation.DoesNotExist:
        conversation = None
        previous_messages = []

    # Render the order detail template with the order, refund history, and conversation messages 
    context = {
        'order': order,
        'refunds': refunds,
        "conversation": conversation,
        "previous_messages": previous_messages,
    }
    return render(request, "order_detail.html", context)