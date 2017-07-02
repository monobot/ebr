# from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet

from api.serializers import TradeSerializer, TradePostSerializer
from api.permissions import IsLogged

from currency.models import Trade


class TradesView(ModelViewSet):
    permission_classes = (IsLogged, )
    serializers = {
        'default': TradeSerializer,
        'list': TradeSerializer,
        'create': TradePostSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_queryset(self):
        return Trade.objects.all()
