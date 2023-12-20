from django.shortcuts import render
from django.http import FileResponse
from .models import Feedback
from django.conf import settings
import os

def DownloadPdf(request):
    pdf = os.path.join('static/assets', 'EdwardZou-Resume.pdf')
    return FileResponse(open(pdf, 'rb'), content_type='application/pdf')

def index(request):
    if request.method == 'POST':
        message = request.POST['message']
        email = request.POST['email']
        name = request.POST['name']
        feedback=Feedback(name=name,email=email,message=message)
        feedback.save()
    return render(request, 'index.html')