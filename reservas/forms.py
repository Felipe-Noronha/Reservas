from django import forms
from .models import Reserva, AreaDeLazer

class ReservaForm(forms.ModelForm):
    area_lazer = forms.ModelChoiceField(queryset=AreaDeLazer.objects.all(), empty_label="Selecione uma area de lazer")
    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Reserva
        fields = ['area_lazer', 'data_inicio', 'data_fim']