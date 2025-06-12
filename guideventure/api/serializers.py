from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Adventure, Question, QuizStep, Step


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'order', 'adventure', 'title', 'description', 'longitude', 'latitude', 'url']
        read_only_fields = ['id']


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'correct_answer', 'wrong_answers']


class QuizStepSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, read_only=False)

    class Meta:
        model = QuizStep
        fields = StepSerializer.Meta.fields + ['questions']
        extra_kwargs = {
            'url': {'view_name': 'step-detail'}
        }


class PolymorphicStepSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, QuizStep):
            return QuizStepSerializer(instance, context=self.context).data
        return StepSerializer(instance, context=self.context).data


class AdventureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'url']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdventureDetailSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Adventure
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'steps']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
