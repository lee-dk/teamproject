from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from .models import Upload, Users
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
    context = Upload(type=type, color=color, datetime=datetime, gender=gender, feature=feature, phone=phone, place=place, photo=photo)
    context.save()

    messages.success(request, "신고 접수 완료되었습니다!")
    return redirect("main_onlyMember")

def search(request):
    page = request.GET.get('page', 1)
    context_list = Upload.objects.all()
    paginator = Paginator(context_list, 3)
    context_listpage = paginator.get_page(page)
    search_list = {"list": context_list}
    return render(request, 'main_onlyMember.html', search_list)

def newLogin(request):
    context = None
    if request.method == "POST":
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        try :
            user = Users.objects.get(useremail=useremail)
        except Users.DoesNotExist :
            context = {'error': '아이디를 확인하세요'}
        else :
            if check_password(password, user.password):
                request.session['user'] = useremail
                messages.success(request, "환영합니다! 로그인이 완료되었습니다!")
                return redirect('main_onlyMember')
            else :
                context = { 'error' : '패스워드를 확인하세요'}
    else :
        if 'user' in request.session:
            context = {'msg': '이미 로그인 하셨습니다.'}
    return render(request, 'main.html', context)

def main_onlyMember(request) :
    # if 'user' in request.session :
        context_list = Upload.objects.all()
        context = {"list": context_list}
        # context =  { 'useremail' : request.session.get('user')}
        return render(request, "main_onlyMember.html", context)
    # else :
    #     context = {'error' : "회원만 볼 수 있는 페이지입니다."}
    #     return render(request, 'main.html', context)


def sign_in(request):
    if request.method =='GET':
        return render(request, 'main.html')
    elif request.method == 'POST':
        useremail = request.POST.get('useremail', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password',None)
        res_data = {}
        if not (username and password and re_password and useremail):
            res_data['error']='아이디 또는 패스워드를 입력해주세요.'
        elif password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
        else:
            users = Users(
                useremail=useremail,
                username=username,
                password=make_password(password),
            )
            users.save()
            messages.success(request, "회원가입이 완료되었습니다!")
            # return redirect('main')

        # return render(request, res_data)
        return render(request, 'main.html', res_data)

def logout(request):
    if 'user' in request.session:
        del request.session['user']
        context = {'msg': '로그아웃 완료'}
    else:
        context = {'msg': '로그인 상태가 아닙니다!'}
    return render(request, 'main.html', context)  ## 초기화면으로 고쳐야 함
