from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from profiles.serializers import RegisterSerializer, LoginSerializer, VerifyOTPSerializer, ResendOTPSerializer, CancelAccountSerializer, CompleteProfileSerializer
from profiles.services import verify_opt_service, resend_otp_service, cancel_account_service, skip_complete_profile_service
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.services import login_service
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken


@api_view(['POST'])
def register_request(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Account created successfully',
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verify_otp_request(request):
    try:
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            verify_opt_service(serializer.validated_data)
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def resend_otp_request(request):
    try:
        serializer = ResendOTPSerializer(data=request.data)

        if serializer.is_valid():
            resend_otp_service(serializer.validated_data)
            return Response({'message': 'New OTP has been sent'}, status=status.HTTP_200_OK)

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def cancel_account_request(request):
    try:
        serializer = CancelAccountSerializer(data=request.data)

        if serializer.is_valid():
            cancel_account_service(serializer.validated_data)
            return Response({'message': 'Account creation has been canceled'}, status=status.HTTP_200_OK)

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_request(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user, profile = login_service(serializer.validated_data)
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Loged in successfully',
                'user': {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'profile': {
                    'birth_date': profile.birth_date,
                    'gender': profile.gender,
                    'phone_number': profile.phone_number,
                    'bio': profile.bio,
                    'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                    'is_profile_complete': profile.is_profile_complete,
                    'skip_is_profile_complete': profile.skip_is_profile_complete
                },
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_request(request):
    try:
        user = request.user
        return Response({
            'message': 'This is a protected route',
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_request(request):
    try:
        token = request.data.get('refresh')

        if token:
            try:
                outstanding_token = OutstandingToken.objects.get(token=token)
                BlacklistedToken.objects.create(token=outstanding_token)

            except OutstandingToken.DoesNotExist:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def skip_complete_profile_request(request):
    try:
        skip_complete_profile_service(request)
        return Response({'message': 'Skipped completing profile'}, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_profile_request(request):
    try:
        serializer = CompleteProfileSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            profile = serializer.save()
            return Response({
                'message': 'Profile completed successfully',
                'profile': {
                    'birth_date': profile.birth_date,
                    'gender': profile.gender,
                    'phone_number': profile.phone_number,
                    'bio': profile.bio,
                    'profile_picture': profile.profile_picture.url if profile.profile_picture.url else None,
                    'is_profile_complete': profile.is_profile_complete,
                    'skip_is_profile_complete': profile.skip_is_profile_complete
                }
            }, status=status.HTTP_201_CREATED)

        for field, messages in serializer.errors.items():
            return Response({'error': messages[0]}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
