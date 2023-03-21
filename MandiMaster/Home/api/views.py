from Home.api import serializers
from Home.models import Room
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Home.api.serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'Get /api/rooms:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getrooms(request):
    rooms = Room.objects.all()
    serializers = RoomSerializer(rooms,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def getroom(request,room_id):
    room = Room.objects.get(id=room_id)
    serializers = RoomSerializer(room,many=False)
    return Response(serializers.data)



