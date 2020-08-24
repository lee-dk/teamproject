from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Upload
import datetime
from django.contrib import messages

# Create your views here.


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(None, request))


def register(request):
    type = request.POST['type']
    color = request.POST['color']
    datetime = request.POST['datetime']
    gender = request.POST['gender']
    feature = request.POST['feature']

    phone = request.POST['phone']
    place = request.POST['place']
    photo = request.FILES['photo']
    context = Upload(type=type, color=color, datetime=datetime, gender=gender, feature=feature,phone=phone,place=place,photo=photo)
    context.save()
    messages.success(request, "신고 접수 완료되었습니다!")
    return redirect("main")
