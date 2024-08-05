# commission/serializers.py

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import (
    InsuranceCompany, Product, Agreement,
    PaymentTerms, CommissionStructure, Transaction, MeetingSummary, Client,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = ['id', 'name', 'contact_info']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PaymentTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerms
        fields = ['id', 'payment_type', 'day_of_month', 'specific_date']

class CommissionStructureSerializer(serializers.ModelSerializer):
    payment_terms = PaymentTermsSerializer()

    class Meta:
        model = CommissionStructure
        fields = ['id', 'product', 'commission_type', 'rate', 'payment_terms']

    def create(self, validated_data):
        payment_terms_data = validated_data.pop('payment_terms')
        payment_terms = PaymentTerms.objects.create(**payment_terms_data)
        return CommissionStructure.objects.create(payment_terms=payment_terms, **validated_data)

class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'agent', 'company', 'created_at']  # Remove 'start_date' if it's not in your model


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'display_name', 'phone_number', 'email', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)
    agent = serializers.PrimaryKeyRelatedField(read_only=True)  # Add this line

    class Meta:
        model = Transaction
        fields = ['id', 'agent', 'client', 'client_id', 'product', 'created_at', 'metadata']
        read_only_fields = ['agent']  # Add this line

class MeetingSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSummary
        fields = '__all__'

class CalculateCommissionSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs