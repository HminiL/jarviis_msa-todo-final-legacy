import datetime
from django.db.models import Q
from django.http import JsonResponse
from icecream import ic
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from event.models import Event
from event.serializer import EventSerializer


@api_view(['GET', 'POST'])
# @parser_classes([JSONParser])
def event_all(request):

    if request.method == 'GET':
        all_event = Event.objects.all()
        serializer = EventSerializer(all_event, many=True)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        request_data = request.data
        request_data['type'] = 'user'
        serializer = EventSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def event_by_user(request, user_id):
    try:
        event = Event.objects.filter(user_id=user_id)
    except Event.DoesNotExist:
        return Response({'message':'Event_DoesNotExis'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(event, many=True)
    return Response(data=serializer.data, status=201)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @parser_classes([JSONParser])
def event_by_id(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({'message':'Event_DoesNotExis'}, status=status.HTTP_404_NOT_FOUND)

    if request.method =='GET':
        serializer = EventSerializer(event)
        return Response(data=serializer.data, status=201)

    elif request.method == 'PUT':
        serializer = EventSerializer(instance=event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': f'<ID_{serializer.data.get("id")}: {serializer.data.get("title")}> 수정완료'}, status=201)
        
    elif request.method =='POST':
        serializer = EventSerializer(event)
        serializer.update(event, request.data)
        return Response({'completion 변경': serializer.data.get("completion")}, status=201)
    
    elif request.method == 'DELETE':
        event.delete()
        return Response({'result': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def event_by_date(request, date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    try:
        event = Event.objects.filter(Q(start__lte=date, end__gte=date) | Q(start=date, end__isnull=True))
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(event, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def event_by_title(request, title):
    try:
        event = Event.objects.filter(title__icontains=title)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(event, many=True)
    return Response(data = serializer.data)

# @api_view(['PUT'])
# def event_state(request, id):
#     try:
#         event = Event.objects.get(pk=id)
#     except Event.DoesNotExist:
#         return Response({'message':'Event_DoesNotExis'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = EventSerializer(instance=event)
#     ic(event, request.data)
#     serializer.update(event,request.data)
#     return Response(data = serializer.data)
#     # if serializer.is_valid():
    #     serializer.save()
    #     return Response(data = serializer.data)
    # return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def get_event_detail2(request):
#     if request.method == "POST":
#         Event.objects.filter(id__gt=3).update(active=True, name='x')
#         print('POST' + '=' * 100)
#         new_event = request.data
#         print(f'{new_event} \n =================')
#         Event.objects.get(_id=new_event).update(active=True, name='x')
#         return Response({'result': f'Welcome,{new_event}'}, status=201)
#
#     return Response({"result":"fail"}, status=status.HTTP_400_BAD_REQUEST)
