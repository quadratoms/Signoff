
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from client_app.models import (
    FormType,
    DynamicFormField,
    DynamicFormFieldValue,
    UserRequest,
    Approval,
)
from .serializers import (
    FormTypeSerializer,
    DynamicFormFieldSerializer,
    DynamicFormFieldValueSerializer,
    UserRequestSerializer,
    UserRequestWithApprovalsSerializer,
    ApprovalSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from app.services.mailservice import send_email


from rest_framework.permissions import AllowAny
from .serializers import SignUpSerializer, UserSerializer
from django.contrib.auth import authenticate, login


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        serialized_user= UserSerializer(user)
        # send_email("subject", "approval_request_template.html", {}, ['quadratoms30@gmail.com', "tquadri@softalliance.com"])

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token, 'data':refresh.__dict__, 'user':serialized_user.data})
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to create or modify objects.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user and request.user.is_staff
        )


class IsOwnerOfApproval(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an approval to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the approval
        return obj.users == request.user




class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']



class FormTypeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer


class FormTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer


class DynamicFormFieldListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = DynamicFormField.objects.all()
    serializer_class = DynamicFormFieldSerializer


class DynamicFormFieldRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = DynamicFormField.objects.all()
    serializer_class = DynamicFormFieldSerializer


class DynamicFormFieldValueListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicFormFieldValue.objects.all()
    serializer_class = DynamicFormFieldValueSerializer


class DynamicFormFieldValueRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicFormFieldValue.objects.all()
    serializer_class = DynamicFormFieldValueSerializer


class UserRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestWithApprovalsSerializer


class UserRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestWithApprovalsSerializer


class ApprovalListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer


class ApprovalDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfApproval]
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer

    # def get_permissions(self):
    #     """
    #     Custom permissions for ApprovalDetailView.
    #     """
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return [permissions.IsAuthenticated()]  # Allow read-only for all authenticated users
    #     else:
    #         return [permissions.IsAuthenticated(), IsOwnerOfApproval()]  # Custom permission for editing approval
