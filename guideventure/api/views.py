from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from .models import Adventure, Step
from .serializers import (AdventureDetailSerializer, AdventureListSerializer,
                          StepSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows steps to be viewed or edited.
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdventureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows adventures to be viewed or edited.
    """
    queryset = Adventure.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return AdventureListSerializer
        return AdventureDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
