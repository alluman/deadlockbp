# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BanPickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'banpick_{self.room_name}'

        # 방 그룹에 가입
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 방 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 클라이언트로부터 메시지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'abox_click':
            box_id = text_data_json['boxId']

            # 방 그룹에 이벤트 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'abox_click',
                    'boxId': box_id
                }
            )

        elif action == 'box_click':
            box_id = text_data_json['boxId']
            image_src = text_data_json['imageSrc']

            # 방 그룹에 이벤트 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'box_click',
                    'boxId': box_id,
                    'imageSrc': image_src
                }
            )

        elif action == 'box_right_click':
            box_id = text_data_json['boxId']
            image_src = text_data_json['imageSrc']

            # 방 그룹에 이벤트 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'box_right_click',
                    'boxId': box_id,
                    'imageSrc': image_src
                }
            )

    # 이벤트 핸들러
    async def abox_click(self, event):
        box_id = event['boxId']

        # 클라이언트에게 이벤트 전송
        await self.send(text_data=json.dumps({
            'action': 'abox_click',
            'boxId': box_id
        }))

    async def box_click(self, event):
        box_id = event['boxId']
        image_src = event['imageSrc']

        # 클라이언트에게 이벤트 전송
        await self.send(text_data=json.dumps({
            'action': 'box_click',
            'boxId': box_id,
            'imageSrc': image_src
        }))

    async def box_right_click(self, event):
        box_id = event['boxId']
        image_src = event['imageSrc']

        # 클라이언트에게 이벤트 전송
        await self.send(text_data=json.dumps({
            'action': 'box_right_click',
            'boxId': box_id,
            'imageSrc': image_src
        }))
