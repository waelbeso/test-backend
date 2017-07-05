from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from accounts.models import User,Address


#"id": "xxx",                  // user id(you can use uuid or the id provided by database, but need to be unique)
#"name": "test",               // user name
#"dob": "",                    // date of birth
#"address": "",                // user address
#"description": "",            // user description
#"created_at": ""              // user created date


class UserAddressSerializer(serializers.ModelSerializer):

    def AddressValidator(value):
        import json
        if "update" in value['method']:
            if value['name']:
                try:
                    Address.objects.get(name=value['name'],user=value['user'])
                except Address.DoesNotExist:
                    return
                address = Address.objects.get(name=value['name'],user=value['user'])
                if str(address.id) in value['pk']:
                    return
                raise serializers.ValidationError('You have Address with this name.')
            raise serializers.ValidationError('Address name is required.')

        if "new" in value['method']:
            if value['name']:
                try:
                    Address.objects.get(name=value['name'],user=value['user'])
                except Address.DoesNotExist:
                    return
                raise serializers.ValidationError('You have Address with this name.')
            raise serializers.ValidationError('Address name is required.')


    name = serializers.JSONField(required=True,
        validators=[AddressValidator ],)

    country = serializers.CharField(required=True)
    province = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    zip_code = serializers.IntegerField(required=True)
    address = serializers.CharField(required=True)


    class Meta:
        model = Address
        fields = ('id', 'name','country','province','city','zip_code','address')

class UserSerializer(serializers.ModelSerializer):

    username         = serializers.CharField(required=False, allow_blank=False)
    dob              = serializers.DateField(required=True)
    description      = serializers.CharField(required=False, allow_blank=False,max_length=None, min_length=None)
    address          = UserAddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username','created_at','dob','description','address',)


class UserRegistrationSerializer(serializers.Serializer):
    
    from rest_framework.validators import UniqueValidator

    def PasswordValidator(value):
        from  django.contrib.auth.password_validation import validate_password
        validate_password(value)

    def UpperCharacterValidator(value):
        import string,re
        UserNameCharacters = word1 = "".join(re.findall("[a-zA-Z]+", value))
        length = len(UserNameCharacters)
        for x in range(0, length):
            if UserNameCharacters[x].upper() == UserNameCharacters[x]:
                raise serializers.ValidationError(_("USER NAME Can't include capital letters."))


    username = serializers.SlugField(required=True, min_length=6, max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all(),
        message= _("That USER NAME is already taken, please select another.")),
        UpperCharacterValidator],)
    
    password = serializers.CharField(required=True, allow_blank=False,
        validators=[PasswordValidator],)


    class Meta:
        model = User
        fields = ('username', 'password')




