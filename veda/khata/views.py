from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,AccountSerializer,DepositeSerializer,LoanSerializer,HeroImageSerializer,VerificationSerializer
from rest_framework import status,views
import jwt,datetime
from .models import User,openaccount,depositetype,applyloan,heroImages,OTP
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser,FormParser
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout,get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import render

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract groups from the data and remove it from the validated data
        groups_data = serializer.validated_data.pop('groups', [])
       
        self.perform_create(serializer)

        # Get the user instance created by perform_create
        user = serializer.instance

        # Handle many-to-many relationships
        if groups_data:
            user.groups.set(groups_data)
        
        verification_link = request.build_absolute_uri(f'/verify/{user.verification_token}/')
        send_mail(
            'Verify your account',
            f'Please verify your account by clicking the following link: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        print(f"email : {email} password {password}")

        if not email or not password:
            return Response({"error":"Email or password are required"},status=status.HTTP_400_BAD_REQUEST)

        user=authenticate(request,email=email,password=password)

        if user is not None:
            if not user.is_verified:
                return Response({"error": "Account is not verified"}, status=status.HTTP_403_FORBIDDEN)

            login(request,user)
            refresh=RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({'refresh':str(refresh),'access':str(refresh.access_token),'user':user_data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"Login failed in valid email or password"},status=status.HTTP_401_UNAUTHORIZED)

  


class UserView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        
        token = request.COOKIES.get('jwt')
       
        print(token)
        if not token:
            print("dint get token")
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
           
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        logout(request)
        return Response({"Success":"Logged out successful"},status=status.HTTP_200_OK)
    
class openbankaccount(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class deposite(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=DepositeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ApplyLoan(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=LoanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class newbankaccdetail(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)  # Print the token for debugging

        if not token:
            print("dint get token")
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            print("User not found")
            raise AuthenticationFailed('Unauthenticated')

        # Query the openaccount model to retrieve user's account data
        account_data = openaccount.objects.all()
        # user = User.objects.filter(id=payload['id']).first()

        if account_data is None:
            print("Account data not found for the user")
            raise AuthenticationFailed('Unauthenticated')

        # Serialize the account data using the openaccountSerializer
        serializer = AccountSerializer(account_data,many=True)

        return Response(serializer.data)

class newdeposite(APIView):
   
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)  # Print the token for debugging

        if not token:
            print("dint get token")
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            print("User not found")
            raise AuthenticationFailed('Unauthenticated')

        # Query the openaccount model to retrieve user's account data
        account_data =depositetype.objects.all()
        # user = User.objects.filter(id=payload['id']).first()

        if account_data is None:
            print("Account data not found for the user")
            raise AuthenticationFailed('Unauthenticated')

        serializer=DepositeSerializer(account_data,many=True)

        return Response(serializer.data)
    

class LendLoan(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)  # Print the token for debugging

        if not token:
            print("dint get token")
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            print("User not found")
            raise AuthenticationFailed('Unauthenticated')

        # Query the openaccount model to retrieve user's account data
        account_data =applyloan.objects.all()
        # user = User.objects.filter(id=payload['id']).first()

        if account_data is None:
            print("Account data not found for the user")
            raise AuthenticationFailed('Unauthenticated')

        serializer=LoanSerializer(account_data,many=True)

        return Response(serializer.data)


class heroimg(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)  # Print the token for debugging

        if not token:
            print("dint get token")
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            print("User not found")
            raise AuthenticationFailed('Unauthenticated')

        # Query the openaccount model to retrieve user's account data
        account_data =heroImages.objects.all()
        # user = User.objects.filter(id=payload['id']).first()

        if account_data is None:
            print("Account data not found for the user")
            raise AuthenticationFailed('Unauthenticated')

        serializer=HeroImageSerializer(account_data,many=True)

        return Response(serializer.data)
    

class uploadimg(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        print(token)  # Print the token for debugging

        if not token:
            print("dint get token")
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            print("User not found")
            raise AuthenticationFailed('Unauthenticated')

        # Query the openaccount model to retrieve user's account data
        account_data =heroImages.objects.all()
        # user = User.objects.filter(id=payload['id']).first()

        if account_data is None:
            print("Account data not found for the user")
            raise AuthenticationFailed('Unauthenticated')
        serializer=HeroImageSerializer(instance=account_data,data=request.data)
        if serializer.is_valid():
            account_data.save()
        return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def uploadimg(request):
    token = request.COOKIES.get('jwt')
    print(token)  # Print the token for debugging

    if not token:
        print("Didn't get a token")
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.filter(id=payload['id']).first()
    if user is None:
        print("User not found")
        raise AuthenticationFailed('Unauthenticated')

    # Create a new instance of the heroImages model
    new_image = heroImages()


    # Set the image field with the request data
    new_image.image = request.data.get('image')

    # Save the new image record
    new_image.save()

    return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def deleteimg(request,pk):
    token = request.COOKIES.get('jwt')
    print(token)  # Print the token for debugging

    if not token:
        print("dint get token")
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        print(f"Decoded Payload: {payload}")  # Print the decoded payload for debugging

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.filter(id=payload['id']).first()
    if user is None:
        print("User not found")
        raise AuthenticationFailed('Unauthenticated')

        # Query the openaccount model to retrieve user's account data
    account_data =heroImages.objects.get(id=pk)
        # user = User.objects.filter(id=payload['id']).first()

    account_data.delete()
    return Response({'message': 'Image Deleted successfully'}, status=status.HTTP_201_CREATED)
    
       
class ResetPasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        current_password=request.data.get('current_password')
        new_password=request.data.get('new_password')

        if not current_password or not new_password:
            return Response({"error":"Current password or new password are required."},status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"error":"Currenet password is incorrect"},status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request,user)

        return Response({"message":"Password reset successfully"},status=status.HTTP_200_OK)

class GeneratedOtpView(APIView):
    def post(self,request):
        email=request.data.get('email')
        if not email:
            return Response({"error":"Email is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=User.objects.get(email=email)
        except:
            return Response({"error":"User with this email doesn't exists"},status=status.HTTP_404_NOT_FOUND)
        otp_instance=OTP.generate_otp(email=email)
        subject='Forgot Passowrd OTP'
        message=f'Your OTP is: {otp_instance.otp}'
        recipient_list=[email]
        from_email=settings.EMAIL_HOST_USER

        try:
            send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            return Response({"message":"OTP sent to your email","isoptsent":True})
        except:
            return Response({"error":"Failed to send otp","isoptsent":False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VerifyOTPView(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp_entered=request.data.get('otp')

        if not email or not otp_entered:
            return Response({"error":"Invalid OTP or email"})
        
        try:
            otp_obj=OTP.objects.get(user__email=email,otp=otp_entered,used=False)
            if otp_obj.used:
                return Response({"error":"OTP has been already been used"},status=status.HTTP_400_BAD_REQUEST)
            elif otp_obj.is_expired():
                return Response({"error":"Invalid OTP or OTP has expired"})
        except OTP.DoesNotExist:
            return Response({"error":"Invalid OTP","isoptverified":True},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Message":"OTP verified successfully","isoptverified":True},status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp_entered=request.data.get('otp')
        password=request.data.get('password')
        if not email or not otp_entered or not password:
            return Response({"error":"Invalid OTP or email "})
        
        try:
            otp_obj=OTP.objects.get(user__email=email,otp=otp_entered,used=False)
            if otp_obj.is_expired():
                return Response({"error":"Invalid OTP or OTP has expired"})
        except OTP.DoesNotExist:
            return Response({"error":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=User.objects.get(email=email)
            user.set_password(password)
            user.save()
            otp_obj.used=True
            otp_obj.save()
            return Response({"message":"Password reset successfully","ispasswordreset":True},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error":"User not found","ispasswordreset":False},status=status.HTTP.HTTP_404_NOT_FOUND)
            
class VerifyAccountView(views.APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            if user.is_verified:
                return render(request, 'verify_success.html', {"message": "Account already verified"})
            user.is_verified = True
            user.save()
            return render(request, 'verify_success.html', {"message": "Account successfully verified"})
        except User.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)