from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Farmer
from .serializers import FarmerSerializer, RegisterSerializer, UserSerializer

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only fetch farmers for the authenticated user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically link the farmer with the logged-in user
        user = self.request.user
        serializer.save(user=user)
        
    def update(self, request, *args, **kwargs):
        """
        Custom update action to update only the farmer profile fields (name, contact, address).
        """
        farmer = self.get_object()
        
        # Ensure that the fields being updated are allowed
        allowed_fields = ['name', 'contact', 'address']
        
        for field in allowed_fields:
            if field in request.data:
                setattr(farmer, field, request.data[field])
        
        farmer.save()
        # Return updated farmer data
        return Response(FarmerSerializer(farmer).data)


class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Handle registration of new user.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "status":"success",
                "message": "User registered successfully."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Handle user login.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            response_data={
                "status":"success",
                "message": "Login successful."
            }
            return Response(response_data, status=200)
        return Response({"message": "Invalid credentials."}, status=400)

