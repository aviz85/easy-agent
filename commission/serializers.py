# commission/serializers.py

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import (
    InsuranceCompany, Product, ProductTransactionSchema, Agreement,
    PaymentTerms, CommissionStructure, Transaction, Commission, MeetingSummary
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

class ProductTransactionSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransactionSchema
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
    company = InsuranceCompanySerializer()
    commission_structures = CommissionStructureSerializer(many=True)

    class Meta:
        model = Agreement
        fields = ['id', 'company', 'start_date', 'end_date', 'terms', 'status', 'commission_structures']

    def validate(self, data):
        errors = {}
        if 'end_date' in data and data['start_date'] > data['end_date']:
            errors['end_date'] = "End date must be after start date."
        if 'commission_structures' not in data or len(data.get('commission_structures', [])) == 0:
            errors['commission_structures'] = "At least one commission structure is required."
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        commission_structures_data = validated_data.pop('commission_structures')
        
        company, _ = InsuranceCompany.objects.get_or_create(name=company_data['name'], defaults=company_data)
        
        agreement = Agreement.objects.create(company=company, **validated_data)
        
        for structure_data in commission_structures_data:
            payment_terms_data = structure_data.pop('payment_terms')
            payment_terms = PaymentTerms.objects.create(**payment_terms_data)
            CommissionStructure.objects.create(agreement=agreement, payment_terms=payment_terms, **structure_data)
        
        return agreement

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)
        commission_structures_data = validated_data.pop('commission_structures', None)

        if company_data:
            company, _ = InsuranceCompany.objects.get_or_create(name=company_data['name'], defaults=company_data)
            instance.company = company

        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.terms = validated_data.get('terms', instance.terms)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if commission_structures_data is not None:
            instance.commission_structures.all().delete()
            for structure_data in commission_structures_data:
                payment_terms_data = structure_data.pop('payment_terms')
                payment_terms = PaymentTerms.objects.create(**payment_terms_data)
                CommissionStructure.objects.create(agreement=instance, payment_terms=payment_terms, **structure_data)

        return instance

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'

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