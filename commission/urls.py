# commission/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, InsuranceCompanyViewSet, ProductViewSet, 
    ProductTransactionSchemaViewSet, AgreementViewSet, PaymentTermsViewSet, 
    CommissionStructureViewSet, TransactionViewSet, CommissionViewSet, 
    MeetingSummaryViewSet, CustomAuthToken, CalculateCommissionView, 
    SubmitMeetingSummaryView, UserRegistrationView, LogoutView,
    UserProfileView, ChangePasswordView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'insurance-companies', InsuranceCompanyViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-transaction-schemas', ProductTransactionSchemaViewSet)
router.register(r'agreements', AgreementViewSet)
router.register(r'payment-terms', PaymentTermsViewSet)
router.register(r'commission-structures', CommissionStructureViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'commissions', CommissionViewSet)
router.register(r'meeting-summaries', MeetingSummaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # Updated this line
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('calculate-commission/', CalculateCommissionView.as_view(), name='calculate-commission'),
    path('submit-meeting-summary/', SubmitMeetingSummaryView.as_view(), name='submit-meeting-summary'),
]