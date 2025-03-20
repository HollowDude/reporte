from rest_framework import viewsets
from app.models import cliente
from app.api.serializers.clienteSerializer import ClienteSerializer
from rest_framework.permissions import IsAuthenticated

class Cliente(viewsets.ModelViewSet):
    queryset = cliente.Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]