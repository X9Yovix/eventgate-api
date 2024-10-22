from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from events.services import get_tags_service


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tags_request(request):
    try:
        tags = get_tags_service()
        return Response({'tags': tags}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_request(request):
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        event = serializer.save(user=request.user)
        return Response({
            'message': 'Event created successfully',
            'event': {
                'id': event.id,
                'event_name': event.event_name,
                'location': event.location,
                'day': event.day,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'images': [image.image.url for image in event.images.all()],
                'tags': [tag.name for tag in event.tags.all()]
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
