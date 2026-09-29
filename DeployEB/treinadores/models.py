from django.db import models

class Treinador(models.Model):
    nome = models.CharField(max_length=100)
    cidade_origem = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class Pokemon(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    nivel = models.PositiveIntegerField()
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE, related_name="pokemons")

    def __str__(self):
        return self.nome