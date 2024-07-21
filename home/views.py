from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PersonModel, Color
from .serializers import PersonSerializer, LoginSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

# class GeeksViewSet(viewsets.ModelViewSet):
#     queryset = GeeksModel.objects.all()
#     serializer_class = GeeksSerializer

# person.object.all()
# [1,2,3] -> queryset

#APIVIEW(class)
class PersonApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        print(request.user)
        obj=PersonModel.objects.all()
        serializer = PersonSerializer(obj, many=True)        
        return Response(serializer.data)
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def put(self, request):
        data = request.data
        obj = PersonModel.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def patch(self, request):
        data=request.data
        obj =PersonModel.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request):
        data=request.data
        obj=PersonModel.objects.get(id=data['id'])
        obj.delete()
        return Response({"message":"person deleted"})

#api_view(decorator)
@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data=serializer.data
        return Response({"message":"success"})
    
    return Response(serializer.errors)

@api_view(['GET','POST','PUT','PATCH','DELETE'])    
def person(request):

    if request.method == 'GET':
        obj=PersonModel.objects.filter(color__isnull =False)
        serializer = PersonSerializer(obj, many=True)        
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer._errors)
    
    elif request.method == 'PUT':
        data = request.data
        obj = PersonModel.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data=request.data
        obj =PersonModel.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else:
        data=request.data
        obj=PersonModel.objects.get(id=data['id'])
        obj.delete()
        return Response({"message":"person deleted"})
    

#ModelViewSet
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = PersonModel.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset=queryset.filter(name__startswith = search)

        serializer = PersonSerializer(queryset, many=True)
        return Response({'status':200, 'data':serializer.data}, status=status.HTTP_204_NO_CONTENT)

#APIVIEW(class)
class LoginAPI(APIView):

    def post(self, request):
        data=request.data
        print("run")
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        print(serializer.data)
        user= authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                'status':False,
                'message':"invalid credencial"
            }, status.HTTP_400_BAD_REQUEST)
        
        token =Token.objects.get_or_create(user=user)
        print(token)

        return Response({'status':True, 'message':'user login', 'Tocken': str(token)},status.HTTP_201_CREATED)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({'status':True, 'message':'user created'}, status.HTTP_201_CREATED)
            