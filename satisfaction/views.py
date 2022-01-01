import requests
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from satisfaction.models import Satisfaction
from satisfaction.serializer import SatisfactionSerializer as Serializer


@api_view(['GET', 'POST'])
def satisfaction_all(request):
    if request.method == 'GET':
        all_satisfaction = Satisfaction.objects.all()
        serializer = Serializer(all_satisfaction, many=True)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': f'"{serializer.data.get("title")}" 입력 완료'}, status=201)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def satisfaction_by_id(request, id):
    try:
        event = Satisfaction.objects.get(pk=id)
    except Satisfaction.DoesNotExist:
        return Response({'message': 'Event_DoesNotExis'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Serializer(event)
        return Response({'result': serializer.data}, status=201)

    elif request.method == 'PUT':
        serializer = Serializer(instance=event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': f'<ID_{serializer.data.get("id")}: {serializer.data.get("title")}> 수정완료'}, status=201)

    elif request.method == 'DELETE':
        event.delete()
        return Response({'result': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def satisfaction_accept(request):
    url = 'http://127.0.0.1:8000/api/suggestion/accept'
    response = requests.get(url)
    data = response.json()
    return Response(data=data)