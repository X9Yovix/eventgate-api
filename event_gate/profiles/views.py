from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from profiles.serializers import RegisterSerializer, LoginSerializer, VerifyOTPSerializer, ResendOTPSerializer, CancelAccountSerializer, CompleteProfileSerializer
from profiles.services import verify_opt_service, resend_otp_service, cancel_account_service, skip_complete_profile_service, complete_profile_service
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.services import login_service
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken


@api_view(['POST'])
def register_request(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
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
        except ValueError as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp_request(request):
    serializer = VerifyOTPSerializer(data=request.data)

    if serializer.is_valid():
        try:
            verify_opt_service(serializer.validated_data)
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resend_otp_request(request):
    serializer = ResendOTPSerializer(data=request.data)

    if serializer.is_valid():
        try:
            resend_otp_service(serializer.validated_data)
            return Response({'message': 'New OTP has been sent'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def cancel_account_request(request):
    serializer = CancelAccountSerializer(data=request.data)

    if serializer.is_valid():
        try:
            cancel_account_service(serializer.validated_data)
            return Response({'message': 'Account creation has been canceled'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_request(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user, profile = login_service(serializer.validated_data)
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
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

        except ValueError as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_request(request):
    user = request.user
    return Response({
        'message': 'This is a protected route',
        'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }, status=status.HTTP_200_OK)


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

    except Exception as e:
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def skip_complete_profile_request(request):
    try:
        skip_complete_profile_service(request)
        return Response({'message': 'Skipped completing profile'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_profile_request(request):
    serializer = CompleteProfileSerializer(data=request.data, context={'user': request.user})

    if serializer.is_valid():
        try:
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
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
