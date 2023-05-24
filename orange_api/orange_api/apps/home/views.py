from django.shortcuts import render,HttpResponse

from rest_framework.views import APIView

from rest_framework.response import Response

# Create your views here.

def home(request):
   return HttpResponse('home')

class TestView(APIView):

   def get(self, request):

      # from django.db import DatabaseError
      # raise DatabaseError("mysql连接失败")
      return Response({'msg': 'hello '})