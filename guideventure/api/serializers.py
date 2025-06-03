from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Adventure, Step


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'adventure', 'title', 'description', 'order', 'longitude', 'latitude', 'url']
        read_only_fields = ['id']


class AdventureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'url']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class AdventureDetailSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Adventure
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'url', 'steps']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
