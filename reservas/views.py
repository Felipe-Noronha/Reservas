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
import matplotlib.pyplot as plt
import base64


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




@login_required
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

    # Gere o gráfico
    plt.pie([data[1] for data in dados_grafico], labels=[data[0] for data in dados_grafico])
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.read()).decode('utf-8')

    # Adicione a imagem ao contexto
    context = {
        'dados_grafico': dados_grafico,
        'areas_lazer': areas_lazer,
        'reservas': reservas,
        'grafico_base64': image_data  # Adicione a variável com a imagem do gráfico
    }

    # Renderize o template com o contexto atualizado
    html = template.render(context)

    # Use o WeasyPrint para gerar o PDF
    pdf_buffer = BytesIO()
    HTML(string=html).write_pdf(pdf_buffer)

    # Define a posição do buffer para o início
    pdf_buffer.seek(0)

    # Cria uma resposta HTTP com o PDF como conteúdo
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=example.pdf'
    return response