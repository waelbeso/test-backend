# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User,Address
from django.http import JsonResponse
from rest_framework.response import Response



# Create your views here.

'''
    Exampel for Get method

    url http://localhost:8000/user/a1489525-6e89-4e92-ad7c-01c367f8c37c
    Response will be json string - >

    {
    "username": "myusss8n5555a877me",
    "created_at": "2017-07-04T23:27:52.255Z",
    "dob": "1983-07-18",
    "description": "Normal description2",
    "address": [
    {
    "id": "5fe52352-00b1-4d16-978e-907c331a1285",
    "name": "home",
    "country": "cn",
    "province": "shanghai",
    "city": "shanghai",
    "zip_code": 113222,
    "address": "room 3454, 221 han si st. "
    },
    {
    "id": "cdcceda9-fffe-41f8-a4ce-5244b7694a47",
    "name": "home2",
    "country": "cn",
    "province": "shanghai",
    "city": "shanghai",
    "zip_code": 113222,
    "address": "room 3454, 221 han si st. "
    }
    ],
    }

    payload exampel for PUT method :
    {"dob":"1983-07-16","description":"Normal description"}

    Response if method put with errors
    "errors":
    { 
    "dob": [ "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."],
    "description": ["This field may not be blank."],
    }
    }

    Request headers exampel:
    Content-Type: application/json
    Authorization: Token a49bb908fbee4873a76c0c14d80358b427eec115

    Response if method DELETE and the user ID is not founded
    {
    "detail": "Not found."
    }

    Response if Invalid token
    {
    "detail": "Invalid token."
    }
    Response if headers not include authentication token response will be
    {
      "detail": "Authentication credentials were not provided."
    }

'''
class UserViewSet(viewsets.ModelViewSet):

    User                   = get_user_model()
    queryset               = User.objects.all()
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
    	from accounts.serializers import UserSerializer
    	data = UserSerializer(request.user).data 
        return JsonResponse(data, status=200)

    def update(self, request, pk=None):
    	from accounts.serializers import UserSerializer
    	import json

    	try:
    		json_data=json.loads(request.body)
    	except ValueError:
    		return JsonResponse({ "errors": "empty payload" }, status=400)

    	json_data=json.loads(request.body)
    	print json_data

    	serializer = UserSerializer(request.user, data=json_data)
    	if serializer.is_valid():
    		serializer.save()
    		return JsonResponse(serializer.data, status=200)
    	return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def delete(self, request, pk=None):
    	from django.http import Http404
    	try:
    		User.objects.get(pk=pk)
    	except User.DoesNotExist:
    		return JsonResponse({ "errors": 'Does not exist' }, status=404,safe=False)
        user = User.objects.get(pk=pk)
        UserID = user.id
        user.delete()

    	return JsonResponse({"deleted":UserID}, status=202)


UserView = UserViewSet.as_view({'get': 'retrieve','put':'update','delete':'delete'})

'''
    payload exampel:
    {"username":"myusername","password":"sda@sdfAAdjj"}

    Request headers exampel:

    Content-Type: application/json

    Response will be json string - >
    If Accepted: { "id": "e8229fc9-ffdb-49e5-afdd-cc46ac9d1cde" }

    or json string include error string for each field
    {
    "username": "That USER NAME is already taken, please select another.",
    "password": "This field may not be blank.",
    }
'''

@csrf_exempt
def Registration(request):
    import json
    from accounts.serializers import UserRegistrationSerializer

    try:
    	json_data=json.loads(request.body)
    except ValueError:
    	return JsonResponse({ "errors": "empty payload" }, status=400)

    json_data = json.loads(request.body)

    if request.method == 'POST':
    	serializer = UserRegistrationSerializer(data=json_data)
    	if serializer.is_valid():
    		user = User.objects.create_user(
                username = serializer.validated_data.get('username'),
                password = serializer.validated_data.get('password'),
                )
    		user.save() 

    		from rest_framework.authtoken.models import Token
    		print dir(Token)
    		token, created = Token.objects.get_or_create(user=user)

    		return JsonResponse({"id":user.id,'token': token.key}, status=201)
    	return JsonResponse(serializer.errors, status=400)
    return JsonResponse({ "errors": "Method is not allowed" }, status=405)


'''
    
    Exampel for post method
    url http://localhost:8000/user/addresses/
    payload exampel:
    {"name":"home","country":"cn","province":"shanghai","city":"shanghai","zip_code":"113222","address":"room 3454, 221 han si st. "}

    Exampel for Get method

    url http://localhost:8000/user/addresses/
     Response will be json string - >
      {
      "id": "5fe52352-00b1-4d16-978e-907c331a1285",
      "name": "home",
      "country": "cn",
      "province": "shanghai",
      "city": "shanghai",
      "zip_code": 113222,
      "address": "room 3454, 221 han si st. "
      },

    Exampel for put method
    url http://localhost:8000/user/addresses/cdcceda9-fffe-41f8-a4ce-5244b7694a47
    payload exampel:
    {"name":"home","country":"cn","province":"shanghai","city":"shanghai","zip_code":"113222","address":"room 3454, 221 han si st. "}


    Exampel for delete method
    url http://localhost:8000/user/addresses/cdcceda9-fffe-41f8-a4ce-5244b7694a47
    Response will be json string - >

'''


class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request):
    	from accounts.serializers import UserAddressSerializer

        address = request.user.address.all()
        serializer = UserAddressSerializer(address, many=True)
        data=serializer.data

        return JsonResponse(data, safe=False, status=200)

    def create(self, request):
    	import json
    	from accounts.serializers import UserAddressSerializer

    	try:
    		json_data=json.loads(request.body)
    	except ValueError:
    		return JsonResponse({ "errors": "empty payload" }, status=400)

        json_data = json.loads(request.body)

        '''
        Address name and user ID are both unique together, 
        so we have to validate address name in a creating and updating method.
        So warb the name field to include user ID and the method (new or updated) 
        will allow us to target them in the Addresses alidator.
        '''
        data = {}
        data['name']     = { "name": json_data["name"] , "user": str(request.user.id) , "method":"new"}
        data['country']  = json_data["country"]
        data['province'] = json_data["province"]
        data['city']     = json_data["city"]
        data['zip_code'] = json_data["zip_code"]
        data['address']  = json_data["address"]

        serializer = UserAddressSerializer(data=data)
        if serializer.is_valid():

            address = Address.objects.create(
                user  = request.user,
                name     = json_data['name'],
                country  = json_data['country'],
                province = json_data['province'],
                city     = json_data['city'],
                zip_code = json_data['zip_code'],
                address  = json_data['address'],
                )
            address.save
            return JsonResponse({'id':address.id,'name': address.name}, status=202)
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def update(self, request,pk):
    	import json
    	from accounts.serializers import UserAddressSerializer

    	try:
    		json_data=json.loads(request.body)
    	except ValueError:
    		return JsonResponse({ "errors": "empty payload" }, status=400)

    	try:
    		Address.objects.get(pk=pk)
    	except Address.DoesNotExist:
    		return JsonResponse({ "errors": 'Does not exist' }, status=404,safe=False)


        json_data = json.loads(request.body)
        '''
        Address name and user ID are both unique together, 
        so we have to validate address name in a creating and updating method.
        So warb the name field to include user ID and the method (new or updated) 
        will allow us to target them in the Addresses alidator.
        '''
        data = {}
        data['name']     = { "name": json_data["name"] , "user": str(request.user.id) , "method":"update","pk":pk }
        data['country']  = json_data["country"]
        data['province'] = json_data["province"]
        data['city']     = json_data["city"]
        data['zip_code'] = json_data["zip_code"]
        data['address']  = json_data["address"]

        serializer = UserAddressSerializer(data=data)

        if serializer.is_valid():

            address          = Address.objects.get(pk=pk)
            address.name     = json_data['name']
            address.country  = json_data['country']
            address.province = json_data['province']
            address.city     = json_data['city']
            address.zip_code = json_data['zip_code']
            address.address  = json_data['address']

            address.save()
            data['name']     = json_data["name"]
            data['id']       = address.id
            return JsonResponse(data, status=202)

        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)


    def delete(self, request,pk):
        from django.http import Http404
        from rest_framework import status

        try:
        	Address.objects.get(pk=pk)
        except Address.DoesNotExist:
        	return JsonResponse({ "errors": 'Does not exist' }, status=404,safe=False)

        address = Address.objects.get(pk=pk)

        if request.user.id == address.user.id:
        	address.delete()
        	return Response(status=status.HTTP_204_NO_CONTENT)

        return JsonResponse({ "errors": 'You have no authority to delete this Address' }, status=400,safe=False)

UserAddressView = AddressViewSet.as_view({'get': 'retrieve','post':'create','put':'update','delete':'delete'})



