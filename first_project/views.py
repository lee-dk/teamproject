from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

# Create your views here.
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(None, request))

def register(request):
    if request.method =='GET':
        return render(request, 'register.html')
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
        return render(request, 'newLogin_1.html', res_data)


def newLogin_1(request):
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
                return redirect('onlymember')
            else :
                context = { 'error' : '패스워드를 확인하세요'}
    else :
        if 'user' in request.session:
            context = {'msg': '이미 로그인 하셨습니다.'}
    return render(request, 'newLogin_1.html', context)  ## 로그인 후 홈페이지로 고쳐야 함

def only_member(request) :
    if 'user' in request.session :
        context =  { 'useremail' : request.session.get('user')}
        return render(request, "homepage.html", context)  ## 로그인 후 페이지로 고쳐야 함
    else :
        context = {'error' : "회원만 볼 수 있는 페이지입니다."}
        return render(request, 'newLogin_1.html', context)

def logout(request):
    if 'user' in request.session :
        del request.session['user']
        context = {'msg' : '로그아웃 완료'}
    else :
        context = {'msg': '로그인 상태가 아닙니다!'}
    return render(request, 'main.html', context)    ## 초기화면으로 고쳐야 함