from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('execute-command/<int:command_id>/', views.execute_command, name='execute_command'),
    path('send-mqtt-message/', views.send_mqtt_message, name='send_mqtt_message'),
    path('subscribe-topic/', views.subscribe_topic, name='subscribe_topic'),
    path('unsubscribe-topic/', views.unsubscribe_topic, name='unsubscribe_topic'),
    path('add-command/', views.add_command, name='add_command'),
    path('delete-command/<int:command_id>/', views.delete_command, name='delete_command'),
    path('api/messages/', views.get_messages_json, name='get_messages_json'),
    path('api/mqtt-status/', views.mqtt_status, name='mqtt_status'),
    path('api/clear-messages/', views.clear_messages, name='clear_messages'),
]
