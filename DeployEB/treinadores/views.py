from django.shortcuts import render
from rest_framework import viewsets
from .models import Treinador, Pokemon
from .serializers import TreinadorSerializer, PokemonSerializer

class TreinadorViewSet(viewsets.ModelViewSet):
    queryset = Treinador.objects.all()
    serializer_class = TreinadorSerializer

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
