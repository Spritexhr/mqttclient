from django.apps import AppConfig

class MqttAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'MQTT应用'
    
    def ready(self):
        # 应用启动时连接MQTT
        from .mqtt_client import mqtt_client
        mqtt_client.connect()
