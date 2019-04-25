from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework import serializers
from FS.models import FS


class FSSerializer(serializers.ModelSerializer):

    class Meta:
        model = FS
        fields = ("__all__" )

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username',"email","password","first_name","last_name")
            extra_kwargs = {'password':{'write_only': True ,"min_length":8}}
        def create(self, validated_data):
            return User.objects.create_user(**validated_data)

        def update(self,instance , validated_data):
            password = validated_data.pop('password',None)
            user = super().update(instance , validated_data)
            if password:
                user.set_password(password)
                user.save()
            return user


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',"password")
    username = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type':'password'},
        trim_whitespace = False
    )
    def validate(self , attrs):
        username =attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username =username,
            password = password,
        )
        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg , code='authentication')
        attrs['user'] = user
        return attrs