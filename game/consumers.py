import json
import os
import asyncio
import requests
import firebase_admin
from firebase_admin import credentials, messaging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

credential_keys = json.loads(os.environ['private_key'])

firebase_cred = credentials.Certificate(credential_keys)
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
        icon = ''
        topic = ''

        if params:
            if 'key' in params:
                key = params['key']
            if 'sessionId' in params:
                session_id = params['sessionId']
            if 'fields' in params:
                fields = params['fields']
                if 'title' in fields:
                    title = fields['title']
                if 'body' in fields:
                    body = fields['body']
                if 'tokens' in fields:
                    tokens = fields['tokens']
                if 'topic' in fields:
                    topic = fields['topic'].replace(' ', '_')
                if 'data' in fields:
                    if fields['data'] != {} and fields['data'] != '':
                        try:
                            data = json.loads(fields['data'])
                        except:
                            parse_response = {
                                'jsonrpc': '2.0',
                                'error': {
                                    'code': 1,
                                    'message': 'Data filed should be JSON format'
                                },
                                'id': id
                            }
                            await self.send_json(parse_response)
                if 'icon' in fields:
                    if fields['icon'] != '':
                        icon = fields['icon']

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
            if icon == '':
                data.update({'title': title, 'body': body})
            else:
                data.update({'title': title, 'body': body, 'icon': icon})

            if key == 'fcmPushNotification':
                message = messaging.MulticastMessage(
                    tokens=tokens,
                    data=data
                )
                print('-------fields---------', fields)
                responses = messaging.send_multicast(message)
                for response in responses.responses:
                    if response.success is False:
                        success = False
                        error_message = str(response.exception)
                        print('---error-log---', error_message)

            elif key == 'subscribeDeviceToTopic':
                subscribe_response = messaging.subscribe_to_topic(tokens, topic)
                # print('------', subscribe_response.errors)
                print(subscribe_response.success_count, '-----tokens were subscribed successfully-------')

            elif key == 'unsubscribeDeviceFromTopic':
                unsubscribe_response = messaging.unsubscribe_from_topic(tokens, topic)
                print(unsubscribe_response.success_count, '-----tokens were unsubscribed successfully-------')

            elif key == 'sendMessageToDevices':
                topic_message = messaging.Message(
                    data=data,
                    topic=topic,
                )
                topic_response = messaging.send(topic_message)
                print('-----------Successfully sent message----------:', topic_response)

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
