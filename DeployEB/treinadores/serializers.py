from rest_framework import serializers
from .models import Treinador, Pokemon

class TreinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treinador
        fields = "__all__"

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = "__all__"