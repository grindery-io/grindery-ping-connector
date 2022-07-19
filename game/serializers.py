from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from common.exception import CustomException

class ConnectorSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True)
    body = serializers.CharField(required=False, allow_blank=True)
    tokens = serializers.ListField(required=True)

    default_error_messages = {
        'empty_tokens': _('Token is empty.'),
    }

    class Meta:
        fields = ("title", "body", "tokens")

    def validate(self, attrs):
        tokens = attrs.get("tokens")

        if not tokens:
            raise CustomException(code=10, message=self.error_messages['empty_tokens'])
        return attrs
