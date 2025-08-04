# MQTT客户端

一个基于Django的Web MQTT客户端，提供图形化界面来管理和执行MQTT命令。

## 功能特性

- 🏠 **首页**: 显示所有预设的MQTT命令按钮，快速执行常用操作
- ⚙️ **管理面板**: 管理MQTT命令、监控消息、订阅主题
- 📡 **实时监控**: 实时显示发送和接收的MQTT消息
- 🎨 **美观界面**: 基于Bootstrap 5的现代化响应式界面
- 🔄 **自动刷新**: 自动刷新消息列表和连接状态

## 安装和运行

### 1. 克隆项目
```bash
git clone <repository-url>
cd mqttclient
```

### 2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install django paho-mqtt
```

### 4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 6. 运行开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 查看应用。

## 使用说明

### 首页功能
- **快捷命令**: 点击预设的命令按钮快速发送MQTT消息
- **快速发送**: 手动输入主题和消息内容发送自定义消息
- **消息日志**: 实时查看最近的MQTT消息记录

### 管理面板功能
- **命令管理**: 添加、编辑、删除MQTT命令
- **主题订阅**: 订阅和取消订阅MQTT主题
- **消息监控**: 查看详细的MQTT消息历史
- **连接状态**: 实时显示MQTT连接状态

### 创建命令
1. 在管理面板点击"添加命令"
2. 填写命令名称、MQTT主题、消息内容
3. 选择按钮颜色和添加描述（可选）
4. 保存后即可在首页使用

## 配置MQTT连接

在 `core/mqtt_client.py` 中配置MQTT服务器连接参数：

```python
MQTT_CONFIG = {
    'broker': 'localhost',  # MQTT服务器地址
    'port': 1883,          # 端口
    'username': None,       # 用户名（可选）
    'password': None,       # 密码（可选）
    'client_id': 'django_mqtt_client'
}
```

## 项目结构

```
mqttclient/
├── core/                 # 主应用
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图函数
│   ├── urls.py          # URL配置
│   ├── admin.py         # 管理后台
│   └── mqtt_client.py   # MQTT客户端
├── templates/           # 模板文件
│   ├── base.html       # 基础模板
│   ├── home.html       # 首页模板
│   └── admin_panel.html # 管理面板模板
└── manage.py           # Django管理脚本
```

## 技术栈

- **后端**: Django 4.2
- **前端**: Bootstrap 5, Font Awesome
- **MQTT**: paho-mqtt
- **数据库**: SQLite (可配置为其他数据库)

## 许可证

MIT License 