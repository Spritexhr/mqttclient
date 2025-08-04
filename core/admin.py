from django.contrib import admin
from .models import MQTTCommand, MQTTMessage

@admin.register(MQTTCommand)
class MQTTCommandAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'button_color', 'created_at']
    list_filter = ['button_color', 'created_at']
    search_fields = ['name', 'topic']

@admin.register(MQTTMessage)
class MQTTMessageAdmin(admin.ModelAdmin):
    list_display = ['topic', 'message_type', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['topic', 'payload']
    readonly_fields = ['timestamp']