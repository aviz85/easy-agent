# commission/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import process_meeting_summary, calculate_commission
from .serializers import (
    MeetingSummarySerializer, TransactionSerializer, UserProfileSerializer,
    ChangePasswordSerializer, UserRegistrationSerializer, UserSerializer,
    InsuranceCompanySerializer, ProductSerializer, AgreementSerializer, PaymentTermsSerializer,
    CommissionStructureSerializer, ClientSerializer
)
from rest_framework import generics, permissions, status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .models import Agreement, InsuranceCompany, CommissionStructure, Product, PaymentTerms, Transaction, MeetingSummary, Client
from django.contrib.auth.models import User
from .serializers import CustomAuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework import viewsets
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.agent == request.user

class AgreementListView(generics.ListAPIView):
    serializer_class = AgreementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Agreement.objects.filter(agent=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send confirmation email
        send_mail(
            'Welcome to Insurance Commission Management System',
            f'Hi {user.username},\n\nYour account has been successfully created. You can now log in to the system.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully. A confirmation email has been sent."
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmitMeetingSummaryView(APIView):
    def post(self, request):
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Meeting summary content is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = process_meeting_summary(request.user, content)
        summary, transaction_data = result[:2]  # Take only the first two values
        
        if not transaction_data:
            # If no transaction was created, create one with basic information
            client = Client.objects.create(display_name="Unknown Client")
            product = Product.objects.first()  # Assuming there's at least one product
            transaction = Transaction.objects.create(
                agent=request.user,
                client=client,
                product=product
            )
        else:
            transaction = Transaction.objects.create(
                agent=request.user,
                client=Client.objects.get_or_create(display_name=transaction_data.get('client_name', 'Unknown Client'))[0],
                product=Product.objects.get_or_create(name=transaction_data.get('product_name', 'Unknown Product'))[0]
            )
        
        response_data = {
            'summary': MeetingSummarySerializer(summary).data,
            'transaction': TransactionSerializer(transaction).data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class CalculateCommissionView(APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            if transaction.agent != request.user and not request.user.is_staff:
                return Response({"error": "You don't have permission to calculate commission for this transaction"}, status=status.HTTP_403_FORBIDDEN)
            commissions = calculate_commission(transaction)
            
            # Serialize the commission data
            serialized_commissions = []
            for commission in commissions:
                serialized_commission = {
                    'transaction': TransactionSerializer(commission['transaction']).data,
                    'commission_structure': CommissionStructureSerializer(commission['commission_structure']).data,
                    'amount': str(commission['amount']),  # Convert Decimal to string
                    'expected_payment_date': commission['expected_payment_date'].isoformat(),
                    'status': commission['status']
                }
                serialized_commissions.append(serialized_commission)
            
            return Response({"commissions": serialized_commissions}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Perform any logout logic here
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class InsuranceCompanyViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AgreementViewSet(viewsets.ModelViewSet):
    serializer_class = AgreementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company']

    def get_queryset(self):
        return Agreement.objects.filter(agent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentTermsViewSet(viewsets.ModelViewSet):
    queryset = PaymentTerms.objects.all()
    serializer_class = PaymentTermsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return PaymentTerms.objects.all()
        return PaymentTerms.objects.filter(agent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class CommissionStructureViewSet(viewsets.ModelViewSet):
    queryset = CommissionStructure.objects.all()
    serializer_class = CommissionStructureSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CommissionStructure.objects.all()
        return CommissionStructure.objects.filter(agent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['agent', 'product', 'created_at']
    search_fields = ['client__display_name']
    ordering_fields = ['created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(agent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MeetingSummaryViewSet(viewsets.ModelViewSet):
    queryset = MeetingSummary.objects.all()
    serializer_class = MeetingSummarySerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]