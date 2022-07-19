from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from common.exception import CustomException


class FieldDataSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True)
    body = serializers.CharField(required=False, allow_blank=True)
    tokens = serializers.ListField(required=True)

    class Meta:
        fields = ("title", "body", "tokens")

    def validate(self, attrs):
        return attrs


class ParamSerializer(serializers.Serializer):
    key = serializers.CharField(required=False)
    fieldData = FieldDataSerializer()

    class Meta:
        fields = ("key", "fieldData", "credentials")

    def validate(self, attrs):
        key = attrs.get("key")
        fieldData = attrs.get("fieldData")
        credentials = attrs.get("credentials")
        # attrs['key'] = key
        # attrs['fieldData'] = fieldData
        # attrs['credentials'] = credentials
        return attrs


class ConnectorSerializer(serializers.Serializer):
    method = serializers.CharField()
    id = serializers.CharField()
    params = ParamSerializer()

    default_error_messages = {
        'invalid_type': _('type is invalid.'),
    }

    class Meta:
        fields = ("params", "method", "id")

    def validate(self, attrs):
        return attrs
