from rest_framework import serializers
from app.models.cliente import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'carnet', 'direccion', 'email', 'telefono']