from django.shortcuts import render

from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET', 'POST'])
def demo_static(request):
    if request.method == 'GET':
        return render(request, 'demo_1/defines/demo_static.html')

@api_view(['GET', 'POST'])
def demo_ansible(request):
    if request.method == 'GET':
        return render(request, 'demo_1/defines/demo_ansible.html')

@api_view(['GET', 'POST'])
def demo_ansible_with_vars(request):
    if request.method == 'GET':
        return render(request, 'demo_1/defines/demo_ansible_with_vars.html')

