# commission/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserProfileView, ChangePasswordView,
    SubmitMeetingSummaryView, CalculateCommissionView, CustomAuthToken,
    LogoutView, UserViewSet, InsuranceCompanyViewSet, ProductViewSet,
    ProductTransactionSchemaViewSet, AgreementViewSet, PaymentTermsViewSet,
    CommissionStructureViewSet, TransactionViewSet, CommissionViewSet,
    MeetingSummaryViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'insurance-companies', InsuranceCompanyViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-transaction-schemas', ProductTransactionSchemaViewSet)
router.register(r'agreements', AgreementViewSet, basename='agreement')
router.register(r'payment-terms', PaymentTermsViewSet)
router.register(r'commission-structures', CommissionStructureViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'commissions', CommissionViewSet)
router.register(r'meeting-summaries', MeetingSummaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('submit-meeting-summary/', SubmitMeetingSummaryView.as_view(), name='submit-meeting-summary'),
    path('calculate-commission/', CalculateCommissionView.as_view(), name='calculate-commission'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]