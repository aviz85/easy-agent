# commission/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import process_meeting_summary, calculate_commission
from .serializers import MeetingSummarySerializer, TransactionSerializer, UserProfileSerializer, ChangePasswordSerializer, CommissionSerializer
from rest_framework import generics, permissions, status
from .serializers import CalculateCommissionSerializer, UserRegistrationSerializer, UserSerializer, InsuranceCompanySerializer, ProductSerializer, ProductTransactionSchemaSerializer, AgreementSerializer, PaymentTermsSerializer, CommissionStructureSerializer, TransactionSerializer, CommissionSerializer, MeetingSummarySerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .models import Agreement, InsuranceCompany, CommissionStructure, Product, ProductTransactionSchema, PaymentTerms, Transaction, Commission, MeetingSummary
from django.contrib.auth.models import User
from .serializers import CustomAuthTokenSerializer

from rest_framework import viewsets
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class AgreementListView(generics.ListAPIView):
    serializer_class = AgreementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Agreement.objects.filter(agent=self.request.user, status='ACTIVE')

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
        summary, transaction = result[:2]  # Take only the first two values
        
        if not transaction:
            # If no transaction was created, create one with basic information
            transaction = Transaction.objects.create(
                agent=request.user,
                client_name="Unknown",  # You might want to extract this from the summary
                status="PENDING"  # Or any default status you prefer
            )
        
        response_data = {
            'summary': MeetingSummarySerializer(summary).data,
            'transaction': TransactionSerializer(transaction).data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class CalculateCommissionView(APIView):
    def post(self, request):
        serializer = CalculateCommissionSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data['transaction_id']
            try:
                transaction = Transaction.objects.get(id=transaction_id)
            except Transaction.DoesNotExist:
                return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

            commissions = calculate_commission(transaction)
            commission_serializer = CommissionSerializer(commissions, many=True)
            return Response(commission_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        # Delete the user's token to log them out
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class InsuranceCompanyViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductTransactionSchemaViewSet(viewsets.ModelViewSet):
    queryset = ProductTransactionSchema.objects.all()
    serializer_class = ProductTransactionSchemaSerializer

class AgreementViewSet(viewsets.ModelViewSet):
    serializer_class = AgreementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company']

    def get_queryset(self):
        return Agreement.objects.filter(agent=self.request.user, status='ACTIVE')

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

class CommissionStructureViewSet(viewsets.ModelViewSet):
    queryset = CommissionStructure.objects.all()
    serializer_class = CommissionStructureSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['agent', 'product', 'status', 'date']
    search_fields = ['client_name']
    ordering_fields = ['date', 'status']

class CommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['transaction__agent', 'commission_structure__product', 'status', 'expected_payment_date']
    search_fields = ['transaction__client_name']
    ordering_fields = ['expected_payment_date', 'amount', 'status']

class MeetingSummaryViewSet(viewsets.ModelViewSet):
    queryset = MeetingSummary.objects.all()
    serializer_class = MeetingSummarySerializer