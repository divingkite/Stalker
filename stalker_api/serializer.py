from rest_framework import serializers
from stalker_api.models import Person,Contest,Question
from django.contrib.auth.models import User

class PersonSerializer(serializers.Serializer):
    '''
    Serializer for stalker_api/models/Person class.
    '''
    cc = serializers.CharField(required=False, allow_blank=True, max_length=20)
    cf = serializers.CharField(required=False, allow_blank=True, max_length=20)
    name = serializers.CharField(required=True)

class UserSerializer(serializers.Serializer):
    '''
    Serializer for django.contrib.auth.User class
    '''
    username = serializers.CharField(max_length=50)
    email    = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
class QuestionSerializer(serializers.Serializer):
    '''
    Serializer for stalker_api/models/Question class
    '''
    name = serializers.CharField(max_length=50)
    link = serializers.CharField(required = False)
    site = serializers.CharField(max_length=20)
    index = serializers.CharField(required=False,max_length=2)
    person = PersonSerializer()
    contest = None

class ContestSerializer(serializers.Serializer):
    '''
    Serializer for stalker_api/models/Contest class
    '''
    pk = serializers.IntegerField()
    contestId = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    site = serializers.CharField(max_length=20)
    question = QuestionSerializer(required=False,many=True)

QuestionSerializer.contest = ContestSerializer()
