from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializers
from rest_framework.permissions import IsAuthenticated

class RegisterAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"User created"},status=status.HTTP_201_CREATED)



class DeleteAccountAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 