from rest_framework import serializers
from .models import PersonModel, Color
from django.contrib.auth.models import User

#these fields used to create a User 
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):

        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is taken')
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('username is taken')

        return data
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
        print(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']

class PersonSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # country = serializers.SerializerMethodField()
    class Meta:
        model = PersonModel
        fields = '__all__'
        #depth = 1

    def get_country(self,obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {'color_name':color_obj.color_name, 'hex_code':'#000'}

    def validate(self, data):

        special_characters = "!@#$%^&*()-=_+><?/"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError("special charector not alowed in name field")

        if data['age'] < 18:
            raise serializers.ValidationError("age should be grater than 18")
        return data