import json
import asyncio
import requests
import firebase_admin
from firebase_admin import credentials, messaging
from channels.generic.websocket import AsyncJsonWebsocketConsumer


firebase_cred = credentials.Certificate('credentials.json')
firebase_app = firebase_admin.initialize_app(firebase_cred)


class SocketAdapter(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_tasks = set()
        self.connected = False

    async def connect(self):
        self.connected = True
        await self.accept()

    async def disconnect(self, close_code):
        self.connected = False
        print('-----socket disconnected-----')

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        request = json.loads(text_data)
        method = request.get("method", None)
        params = request.get("params", None)
        id = request.get("id", None)
        title = ''
        body = ''
        tokens = []
        data = {}
        fields = ''
        session_id = ''
        key = ''

        if params:
            if 'key' in params:
                key = params['key']
            if 'sessionId' in params:
                session_id = params['sessionId']
            if 'fields' in params:
                fields = params['fields']
                title = fields['title']
                body = fields['body']
                tokens = fields['tokens']
                if 'data' in fields:
                    data = json.loads(fields['data'])

        if method == 'ping':
            response = {
                'jsonrpc': '2.0',
                'result': {},
                'id': id
            }
            await self.send_json(response)

        if method == 'runAction':
            success = True
            error_message = ''

            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                tokens=tokens,
                data=data
            )
            responses = messaging.send_multicast(message)
            for response in responses.responses:
                if response.success is False:
                    success = False
                    error_message = response.exception
                    print('---error-log---', error_message)

            if success:
                run_action_response = {
                    'jsonrpc': '2.0',
                    'result': {
                        'key': key,
                        'sessionId': session_id,
                        'payload': fields
                    },
                    'id': id
                }
            else:
                run_action_response = {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 1,
                        'message': error_message
                    },
                    'id': id
                }
            await self.send_json(run_action_response)
