from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from events.services import get_tags_service, get_recent_events_service, get_event_service


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tags_request(request):
    try:
        tags = get_tags_service()
        return Response({'tags': tags}, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_request(request):
    try:
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

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_events_request(request):
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 5)

    try:
        events, total_pages = get_recent_events_service(page=int(page), page_size=int(page_size))
        return Response({
            "events": events,
            "total_pages": total_pages,
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_request(request):
    try:
        id = request.query_params.get('id')
        event = get_event_service(id)
        return Response({
            "event": event,
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
