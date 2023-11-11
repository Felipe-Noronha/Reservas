from django.db import models

class AreaDeLazer(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()


    def __str__(self):
        return self.nome

class Reserva(models.Model):
    area_lazer = models.ForeignKey(AreaDeLazer, on_delete = models.CASCADE)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()    

 