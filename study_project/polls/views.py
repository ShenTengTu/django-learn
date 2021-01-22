from django.http import HttpResponse


def index(request):
    return HttpResponse("民意調查首頁")
