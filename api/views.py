from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import todos
from api.serializers import RegistrationSerializer, todoSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class todosView(ViewSet):


    def list(self,request,*args,**kw):
        qs=todos.objects.all()
        serializer=todoSerializer(qs,many=True)
        return Response(data=serializer.data)


    def create(self,request,*args,**kw):
        serializer=todoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    def retrieve(self,request,*args,**kw):
        id=kw.get('pk')
        qs=todos.objects.get(id=id)
        serializer=todoSerializer(qs,many=False)
        return Response(data=serializer.data)


    def destroy(self,request,*args,**kw):
        id=kw.get('pk')
        todos.objects.get(id=id.delete)
        return Response(data='deleted')


    def update(self,request,*args,**kw):
        id=kw.get('pk')
        object=todos.objects.get(id=id)
        serializer=todoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)





class todosModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]




    serializer_class=todoSerializer
    queryset=todos.objects.all()


    def get_queryset(self):
        return todos.objects.filter(user=self.request.user)
        

    def create(self,request,*args,**kw):
        serializer=todoSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    


    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)  


    def create(self, request, *args, **kwargs):
        Serializer=todoSerializer(data=request.data)
        if Serializer.is_valid():
            todos.objects.create(**Serializer.validated_data,user=request.user)
            return Response(data=Serializer.data)
        else:
            return Response(data=Serializer.errors)    
    

    @action(methods=['GET'],detail=False)                                
    def pending_todos(self,request,*args,**kw):
        qs=todos.objects.filter(status=False)
        serializer=todoSerializer
        return Response(data=serializer.data)

    @action(methods=['GET'],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=todos.objects.filter(status=True)
        serializer=todoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=['POST'],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get('pk')
        object=todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=todoSerializer(object,many=False)
        return Response(data=serializer.data)


class UsersView(ModelViewSet):

    serializer_class=RegistrationSerializer
    queryset=User.objects.all()


    # def create(self, request, *args, **kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors) 










