from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from user.models import User
from user.api.serializers import RegistrationSerializer,LoginSerializer
from random import choice
from string import ascii_letters
import itertools
from django.core.mail import EmailMessage,send_mail



# @api_view(['POST'])
# def registration_view(request):
#     if request.method == "POST":
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = 'Success'
#             data['username'] = user.username
#             data['email'] = user.email
#             data['fullname'] = user.fullname
#             token, created = Token.objects.get_or_create(user=user)
#             data['token'] = str(token.key)
#         else:
#             data = serializer.errors
#         return Response(data)

@api_view(['POST'])
def login(request):
    data={}
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data['satus']= 'success'
        data['token']= token.key
    else:
        data = serializer.errors
        data['status']='fail'

    return Response(data)


@api_view(['POST'])
def Register(request):
    data={}
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        token, created = Token.objects.get_or_create(user=user) 
        data['satus']= 'success'
        data['token']= token.key
        data['username']= user.username
    else:
        data = serializer.errors
        data['status']='fail'

    return Response(data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated,])
def Logout(request):
    data = {}
    try:
        token=Token.objects.get(user=request.user)
        token.delete()
        data['status'] = 'success'
        data['user'] = request.user.username 
    except Token.DoesNotExist:
        data['status'] = 'fail'

    return Response(data)



def set_resetter():
    size = choice([10,11,12])
    entity=ascii_letters+'123456789'
    value=''
    for  i in itertools.count(1):
        for i in range(0,size):
            pick = str(choice(entity))
            value+=pick
        if value not in User.objects.filter(resetter=value).values_list('resetter',flat=True):
            break
        set_resetter()
    return value

@api_view(['POST'])
def forgotpassword(request):
    data = {}
    user_name=request.data['username']
    email = request.data['email']

    try:
        user=User.objects.get(username=user_name,email=email)
        token, created = Token.objects.get_or_create(user=user)
        if created:
            token.delete()
            token = Token.objects.create(user=user)
        token.save()
        reset_val=set_resetter()
        """email_subject='Hi {}, Request to Reset Password'.format(user.fullname)
        email_body='we received a request to reset your account password.If this request was not made by you kindly ignore as your account is safe with us.\nIf the request was made by you kindly make use of the code below.\n\n\n{}'.format(reset_val)
        email = EmailMessage(
                                email_subject,
                                email_body,
                                'officialswiftstand@gmail.com',
                                [user.email],
                            )
        email.send(fail_silently=False)"""
        user.resetter='123456789abc'
        user.save(update_fields=['resetter'])
        data['status'] = 'success'
        data['token'] = token.key
    
    except User.DoesNotExist:
        data['status'] = 'fail'
        data['info'] = 'The infos provided does not match/exist in our system'
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def confirm_reset(request):
    data = {}
    user=request.user
    token=Token.objects.get(user=request.user)
    provided_resetter=request.data['code']
    if provided_resetter == user.resetter:
        new_password = request.data['password']
        user.set_password(new_password)
        user.resetter=''
        user.save()
        data['status']='success'
        data['token']=token.key
        data['username']=user.username
    else:
        data['status']='fail'
        data['info']='The code entered is wrong, Try again!'
    
    return Response(data)

