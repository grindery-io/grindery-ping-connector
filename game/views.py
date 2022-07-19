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

        title = serializer.data.get('title')
        body = serializer.data.get('body')
        tokens = serializer.data.get('tokens')

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            tokens=tokens
        )
        responses = messaging.send_multicast(message)
        for response in responses.responses:
            print(response)
        print('11111111111111111111')
        print(responses.success_count)

        return Response(
            {
                True
            },
            status=status.HTTP_201_CREATED
        )
