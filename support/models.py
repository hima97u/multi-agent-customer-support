from django.db import models
from django.contrib.auth.models import User
from orders.models import Order



class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation #{self.id} - {self.user.username} / Order #{self.order.id}"
    
    @property # to be treaded as a field of conversation model, so we can access it like conversation.manager_involvement instead of conversation.manager_involvement() in templates
    def manager_involvement(self):
        # this is reverse lookup to check if there is any manager involvement in the conversation or not
        return self.agentlogs.filter(event_type="manager").exists()


    @property # to be treaded as a field of conversation model, so we can access it like conversation.risk_assessment_involvement instead of conversation.risk_assessment_involvement() in templates
    def risk_assessment_involvement(self):
        # this is reverse lookup to check if there is any risk assessment involvement in the conversation or not
        return self.agentlogs.filter(event_type="risk").exists()

class Message(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("agent", "Agent"),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}" # Agent: We are checking your request, please wait...

    

class AgentLog(models.Model):
    # These event types are the dashboard audit trail for the 3 agents plus their tool activity.
    EVENT_CHOICES = [
        ("support", "Support Agent"),
        ("tool_call", "Tool Call"),
        ("tool_result", "Tool Result"),
        ("manager", "Manager Agent"),
        ("risk", "Risk Agent"),
        ("final", "Final Reply"),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="agentlogs")
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.event_type}] - {self.message[:40]}"