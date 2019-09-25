from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DeployResult(AsyncWebsocketConsumer):
    async def connect(self):
        self.service_uid = 1111
        self.chat_group_name = 'chat_%s' % self.service_uid
        # 收到连接时候处理，
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 关闭channel时候处理
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # 收到消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
        print("收到消息--》",message)
        # 发送消息到组
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'client.message',
                'message': message
            }
        )

    # 处理客户端发来的消息
    async def client_message(self, event):
        message = event['message']
        print("发送消息。。。",message)
        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))