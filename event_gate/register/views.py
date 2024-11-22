from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from register.services import interested_in_event, request_to_join_event, cancel_request, accept_request, remove_interest, check_user_event_status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def interested_in_event_request(request):
    event_id = request.query_params.get('event_id')
    user = request.user
    try:
        interested_in_event(user, event_id)
        return Response({
            'message': 'Interest in event created successfully'
        }, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_interest_request(request):
    event_id = request.query_params.get('event_id')
    user = request.user
    try:
        remove_interest(user, event_id)
        return Response({"message": "Interest removed successfully"}, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_to_join_event_request(request):
    event_id = request.query_params.get('event_id')
    user = request.user
    try:
        request_to_join_event(user, event_id)
        return Response({
            'message': 'Request to join event sent successfully'
        }, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_request_request(request):
    event_id = request.query_params.get('event_id')
    user = request.user
    try:
        cancel_request(user, event_id)
        return Response({"message": "Request cancelled successfully"}, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_request_request(request):
    event_id = request.query_params.get('event_id')
    user_id = request.query_params.get('user_id')
    user = request.user
    if not event_id or not user_id:
        return Response({'error': 'IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        accept_request(auth_user=user, user_id=user_id, event_id=event_id)
        return Response({"message": "Request accepted successfully"}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_event_status_request(request):
    event_id = request.query_params.get('event_id')
    user = request.user
    if not event_id:
        return Response({'error': 'Event ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        status_data = check_user_event_status(user, event_id)
        return Response(status_data, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
