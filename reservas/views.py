from django.shortcuts import render, redirect
from .models import AreaDeLazer, Reserva
from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from weasyprint import HTML


def index(request):
    areas_lazer = AreaDeLazer.objects.all()
    reservas = Reserva.objects.all()

    # Crie uma lista de dados no formato (área, quantidade de reservas)
    dados_grafico = []

    for area in areas_lazer:
        # Substitua isso pela lógica real para contar as reservas para cada área
        reservas_count = Reserva.objects.filter(area_lazer=area).count()
        dados_grafico.append([area.nome, reservas_count])

    return render(request, 'reservas/index.html', {'areas_lazer': areas_lazer, 'reservas': reservas, 'dados_grafico': dados_grafico})


@login_required
def fazer_reserva(request):
    form = ReservaForm()

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return redirect('index')
        else:
            form = ReservaForm()
    return render(request, 'reservas/fazer_reserva.html',{'form': form})




def generate_pdf(request):
    # Renderiza o template HTML em um contexto
    template = get_template('reservas/index.html')  

    areas_lazer = AreaDeLazer.objects.all()
    reservas = Reserva.objects.all()
    
    dados_grafico = []

    for area in areas_lazer:
        # Substitua isso pela lógica real para contar as reservas para cada área
        reservas_count = Reserva.objects.filter(area_lazer=area).count()
        dados_grafico.append([area.nome, reservas_count])

    html = template.render({ 'dados_grafico': dados_grafico, 'areas_lazer': areas_lazer, 'reservas': reservas})  

    # Cria um buffer de bytes para armazenar o PDF
    buffer = BytesIO()

    # Use o WeasyPrint para gerar o PDF
    HTML(string=html).write_pdf(buffer)

    # Define a posição do buffer para o início
    buffer.seek(0)

    # Cria uma resposta HTTP com o PDF como conteúdo
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=example.pdf'
    return response