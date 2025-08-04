from django.db import models
import json

class MQTTCommand(models.Model):
    name = models.CharField(max_length=100, verbose_name="命令名称")
    topic = models.CharField(max_length=200, verbose_name="主题")
    payload = models.TextField(verbose_name="消息内容")
    description = models.TextField(blank=True, verbose_name="描述")
    button_color = models.CharField(
        max_length=20, 
        default='btn-primary',
        choices=[
            ('btn-primary', '蓝色'),
            ('btn-success', '绿色'),
            ('btn-danger', '红色'),
            ('btn-warning', '黄色'),
            ('btn-info', '青色'),
        ],
        verbose_name="按钮颜色"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "MQTT命令"
        verbose_name_plural = "MQTT命令"
    
    def __str__(self):
        return self.name
    
    def get_payload_dict(self):
        try:
            return json.loads(self.payload)
        except:
            return {"msg": self.payload}


class MQTTMessage(models.Model):
    MESSAGE_TYPES = [
        ('sent', '发送'),
        ('received', '接收'),
    ]
    
    topic = models.CharField(max_length=200, verbose_name="主题")
    payload = models.TextField(verbose_name="消息内容")
    message_type = models.CharField(
        max_length=10, 
        choices=MESSAGE_TYPES,
        default='received',
        verbose_name="消息类型"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")
    
    class Meta:
        verbose_name = "MQTT消息"
        verbose_name_plural = "MQTT消息"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.topic} - {self.timestamp}"
