from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import MQTTCommand, MQTTMessage
from .mqtt_client import mqtt_client
import json
import logging

logger = logging.getLogger(__name__)

def home(request):
    """首页 - 显示所有MQTT命令按钮"""
    commands = MQTTCommand.objects.all().order_by('created_at')
    recent_messages = MQTTMessage.objects.all().order_by('-timestamp')[:10]
    
    context = {
        'commands': commands,
        'recent_messages': recent_messages,
        'mqtt_connected': mqtt_client.connected,
    }
    return render(request, 'home.html', context)

def admin_panel(request):
    """管理面板"""
    commands = MQTTCommand.objects.all().order_by('-created_at')
    messages = MQTTMessage.objects.all().order_by('-timestamp')[:50]
    
    context = {
        'commands': commands,
        'messages': messages,
        'mqtt_connected': mqtt_client.connected,
        'subscribed_topics': list(mqtt_client.subscribed_topics),
    }
    return render(request, 'admin_panel.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def execute_command(request, command_id):
    """执行MQTT命令"""
    try:
        command = get_object_or_404(MQTTCommand, id=command_id)
        
        # 发送MQTT消息
        success = mqtt_client.publish(command.topic, command.payload)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': f'命令 "{command.name}" 执行成功',
                'topic': command.topic,
                'payload': command.payload
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '命令执行失败，请检查MQTT连接'
            })
    
    except Exception as e:
        logger.error(f"执行命令失败: {e}")
        return JsonResponse({
            'success': False,
            'message': f'执行失败: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def send_mqtt_message(request):
    """发送自定义MQTT消息"""
    try:
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        payload = data.get('payload', '').strip()
        
        if not topic:
            return JsonResponse({'success': False, 'message': '主题不能为空'})
        
        if not payload:
            return JsonResponse({'success': False, 'message': '消息内容不能为空'})
        
        # 尝试解析payload为JSON
        try:
            json.loads(payload)
        except:
            # 如果不是JSON，直接作为字符串发送
            pass
        
        success = mqtt_client.publish(topic, payload)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': '消息发送成功'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '消息发送失败'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'发送失败: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def subscribe_topic(request):
    """订阅MQTT主题"""
    try:
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        
        if not topic:
            return JsonResponse({'success': False, 'message': '主题不能为空'})
        
        success = mqtt_client.subscribe(topic)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': f'已订阅主题: {topic}'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '订阅失败'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'订阅失败: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def unsubscribe_topic(request):
    """取消订阅MQTT主题"""
    try:
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        
        if not topic:
            return JsonResponse({'success': False, 'message': '主题不能为空'})
        
        success = mqtt_client.unsubscribe(topic)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': f'已取消订阅主题: {topic}'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '取消订阅失败'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'取消订阅失败: {str(e)}'
        })

def add_command(request):
    """添加新命令"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            topic = request.POST.get('topic', '').strip()
            payload = request.POST.get('payload', '').strip()
            description = request.POST.get('description', '').strip()
            button_color = request.POST.get('button_color', 'btn-primary')
            
            if not all([name, topic, payload]):
                messages.error(request, '命令名称、主题和消息内容不能为空')
                return redirect('admin_panel')
            
            # 验证payload是否为有效JSON
            try:
                json.loads(payload)
            except:
                # 如果不是JSON，包装成JSON
                payload = json.dumps({"msg": payload}, ensure_ascii=False)
            
            MQTTCommand.objects.create(
                name=name,
                topic=topic,
                payload=payload,
                description=description,
                button_color=button_color
            )
            
            messages.success(request, f'命令 "{name}" 添加成功')
            return redirect('admin_panel')
        
        except Exception as e:
            messages.error(request, f'添加命令失败: {str(e)}')
            return redirect('admin_panel')
    
    return redirect('admin_panel')

def delete_command(request, command_id):
    """删除命令"""
    try:
        command = get_object_or_404(MQTTCommand, id=command_id)
        command_name = command.name
        command.delete()
        messages.success(request, f'命令 "{command_name}" 已删除')
    except Exception as e:
        messages.error(request, f'删除命令失败: {str(e)}')
    
    return redirect('admin_panel')

def get_messages_json(request):
    """获取最新消息的JSON数据"""
    messages = MQTTMessage.objects.all().order_by('-timestamp')[:20]
    
    data = []
    for msg in messages:
        data.append({
            'id': msg.id,
            'topic': msg.topic,
            'payload': msg.payload,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'message_type': msg.message_type,
        })
    
    return JsonResponse({'messages': data})

def mqtt_status(request):
    """获取MQTT连接状态"""
    return JsonResponse({
        'connected': mqtt_client.connected,
        'subscribed_topics': list(mqtt_client.subscribed_topics)
    })

@csrf_exempt
@require_http_methods(["POST"])
def clear_messages(request):
    """清空所有消息记录"""
    try:
        # 获取要清空的消息数量
        count = MQTTMessage.objects.count()
        
        # 清空所有消息
        MQTTMessage.objects.all().delete()
        
        logger.info(f"已清空 {count} 条消息记录")
        
        return JsonResponse({
            'success': True,
            'message': f'已清空 {count} 条消息记录',
            'cleared_count': count
        })
    
    except Exception as e:
        logger.error(f"清空消息失败: {e}")
        return JsonResponse({
            'success': False,
            'message': f'清空消息失败: {str(e)}'
        })
