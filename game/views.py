import json
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import credentials, messaging

from .serializers import ConnectorSerializer

firebase_cred = credentials.Certificate('credentials.json')
firebase_app = firebase_admin.initialize_app(firebase_cred)


class FCMMessagerView(GenericAPIView):
    serializer_class = ConnectorSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        params = serializer.data.get('params')
        method = serializer.data.get('method')
        request_id = serializer.data.get('id')
        key = params['key']

        title = params['fieldData']['title']
        body = params['fieldData']['body']
        tokens = params['fieldData']['tokens']

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            tokens=tokens
        )
        messaging.send_multicast(message)

        return Response(
            {
                "jsonrpc": "2.0",
                "method": method,
                "id": request_id,
                "params": {
                    "key": key,
                    "fieldData": {
                        "title": title,
                        "body": body,
                        "tokens": tokens
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )
