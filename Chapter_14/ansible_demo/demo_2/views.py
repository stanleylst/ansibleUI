from django.shortcuts import render

from rest_framework.decorators import api_view


# Create your views here.


@api_view(['GET', 'POST'])
def demo_server_deploy(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_server_deploy.html')

@api_view(['GET', 'POST'])
def demo_server_create(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_server_create.html')

@api_view(['GET', 'POST'])
def demo_server_add(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_server_add.html')

@api_view(['GET', 'POST'])
def demo_server_delete(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_server_delete.html')

@api_view(['GET', 'POST'])
def demo_server_modify(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_server_modify.html')

@api_view(['GET', 'POST'])
def demo_read_log(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_read_log.html')

@api_view(['GET', 'POST'])
def demo_upload(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_upload.html')

@api_view(['GET', 'POST'])
def demo_config_center(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_config_center.html')

@api_view(['GET', 'POST'])
def demo_operate_interface(request):
    if request.method == 'GET':
        return render(request, 'demo_2/defines/demo_operate_interface.html')