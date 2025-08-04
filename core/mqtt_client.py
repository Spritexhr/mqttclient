import paho.mqtt.client as mqtt
import json
import logging
from django.conf import settings
from .models import MQTTMessage
import threading

logger = logging.getLogger(__name__)

class MQTTClientManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # 设置认证信息
        if hasattr(settings, 'MQTT_USERNAME') and settings.MQTT_USERNAME:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        
        self.connected = False
        self.subscribed_topics = set()
        self._initialized = True
    
    def connect(self):
        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST, 
                settings.MQTT_BROKER_PORT, 
                60
            )
            self.client.loop_start()
            logger.info("MQTT客户端连接中...")
        except Exception as e:
            logger.error(f"MQTT连接失败: {e}")
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("MQTT客户端已连接")
            # 重新订阅之前的主题
            for topic in self.subscribed_topics:
                client.subscribe(topic)
        else:
            logger.error(f"MQTT连接失败，错误代码: {rc}")
    
    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            logger.info(f"收到消息: {topic} - {payload}")
            
            # 保存接收到的消息
            MQTTMessage.objects.create(
                topic=topic,
                payload=payload,
                message_type='received'
            )
        except Exception as e:
            logger.error(f"处理接收消息失败: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.info("MQTT客户端已断开连接")
    
    def publish(self, topic, payload):
        try:
            if not self.connected:
                self.connect()
            
            if isinstance(payload, dict):
                payload = json.dumps(payload, ensure_ascii=False)
            
            result = self.client.publish(topic, payload)
            
            if result.rc == 0:
                # 保存发送的消息
                MQTTMessage.objects.create(
                    topic=topic,
                    payload=payload,
                    message_type='sent'
                )
                logger.info(f"消息已发送: {topic} - {payload}")
                return True
            else:
                logger.error(f"消息发送失败，错误代码: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
    
    def subscribe(self, topic):
        try:
            if not self.connected:
                self.connect()
            
            self.client.subscribe(topic)
            self.subscribed_topics.add(topic)
            logger.info(f"已订阅主题: {topic}")
            return True
        except Exception as e:
            logger.error(f"订阅主题失败: {e}")
            return False
    
    def unsubscribe(self, topic):
        try:
            self.client.unsubscribe(topic)
            self.subscribed_topics.discard(topic)
            logger.info(f"已取消订阅主题: {topic}")
            return True
        except Exception as e:
            logger.error(f"取消订阅失败: {e}")
            return False

# 获取全局MQTT客户端实例
mqtt_client = MQTTClientManager()
