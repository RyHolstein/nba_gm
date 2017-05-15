from django.shortcuts import render
#from apps.login_reg.models import User
# Create your views here.

def home(request):
    context = {
        #'user': User.objects.get(id=request.session.id)
    }
    return render(request, 'mainapp/index.html', context)
