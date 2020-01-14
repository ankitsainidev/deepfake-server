from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import api_view
from .manager import assign_next, update_time, close


@api_view(['GET', 'POST'])
def starter(request):
    if request.method == 'GET':
        respons = assign_next()
        return Response(respons)
    if request.method == 'POST':
        respons = assign_next(request.data['part'])



@api_view(['POST'])
def notify(request):
    part,block = request.data['part'],request.data['block']
    update_time(part,block)
    return Response({})


@api_view(['POST'])
def completed(request):
    link,part,block = request.data['link'],request.data['part'],request.data['block']
    close(part,block,link)
    return Response({})
