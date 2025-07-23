from rest_framework import viewsets, permissions
from .models import EmployeeProfile, Outlet
from .serializers import EmployeeProfileSerializer, OutletSerializer,EmployeeProfileReadOnlySerializer

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # adjust as needed

class OutletViewSet(viewsets.ModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer

class EmployeeProfileReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileReadOnlySerializer
    permission_classes = [permissions.IsAuthenticated]  # or change as needed