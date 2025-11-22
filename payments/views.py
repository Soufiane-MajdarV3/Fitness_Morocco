"""
Subscription and billing API endpoints
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import (
    SubscriptionPlan, Organization, TrainerSubscription, BillingSubscription,
    OrganizationInvitation, Invoice
)
from .services import SubscriptionService, OrganizationService, CommissionService
from .serializers import (
    SubscriptionPlanSerializer, OrganizationSerializer, TrainerSubscriptionSerializer,
    OrganizationInvitationSerializer, InvoiceSerializer
)


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Subscription plans - read only for users"""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = []  # Public
    
    @action(detail=False, methods=['get'])
    def trainer_plans(self, request):
        """Get all available trainer plans"""
        plans = SubscriptionPlan.objects.filter(is_active=True, is_org_plan=False)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def organization_plans(self, request):
        """Get all available organization plans"""
        plans = SubscriptionPlan.objects.filter(is_active=True, is_org_plan=True)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)


class TrainerSubscriptionViewSet(viewsets.ViewSet):
    """Trainer subscription management"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_subscription(self, request):
        """Get current user's subscription"""
        try:
            subscription = TrainerSubscription.objects.get(trainer=request.user)
            serializer = TrainerSubscriptionSerializer(subscription)
            return Response(serializer.data)
        except TrainerSubscription.DoesNotExist:
            return Response({'detail': 'No subscription found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def start_trial(self, request):
        """Start free trial for Basic plan"""
        try:
            basic_plan = SubscriptionPlan.objects.get(key='basic')
            subscription = SubscriptionService.create_trainer_subscription(
                request.user, 'basic', is_trial=True
            )
            serializer = TrainerSubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def upgrade_plan(self, request):
        """Upgrade to a paid plan"""
        plan_key = request.data.get('plan_key')
        if not plan_key:
            return Response({'detail': 'plan_key required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscription = SubscriptionService.upgrade_trainer_plan(request.user, plan_key)
            serializer = TrainerSubscriptionSerializer(subscription)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def cancel(self, request):
        """Cancel subscription"""
        try:
            subscription = TrainerSubscription.objects.get(trainer=request.user)
            subscription.is_active = False
            subscription.save()
            serializer = TrainerSubscriptionSerializer(subscription)
            return Response(serializer.data)
        except TrainerSubscription.DoesNotExist:
            return Response({'detail': 'No subscription found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def earnings_summary(self, request):
        """Get trainer earnings summary"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        summary = CommissionService.get_trainer_earnings_summary(request.user, start_date, end_date)
        return Response(summary)


class OrganizationViewSet(viewsets.ModelViewSet):
    """Organization (gym/club) management"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    
    def get_queryset(self):
        """Users see only their organization"""
        return Organization.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Create organization for current user"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def invite_trainer(self, request, pk=None):
        """Invite a trainer to the organization"""
        organization = self.get_object()
        email = request.data.get('email')
        
        if not email:
            return Response({'detail': 'email required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invitation = OrganizationService.invite_trainer(organization, email, request.user)
            serializer = OrganizationInvitationSerializer(invitation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def trainers(self, request, pk=None):
        """List trainers in this organization"""
        organization = self.get_object()
        trainers = TrainerSubscription.objects.filter(organization=organization)
        serializer = TrainerSubscriptionSerializer(trainers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def remove_trainer(self, request, pk=None):
        """Remove a trainer from the organization"""
        organization = self.get_object()
        trainer_id = request.data.get('trainer_id')
        
        if not trainer_id:
            return Response({'detail': 'trainer_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            trainer_user = User.objects.get(id=trainer_id)
            OrganizationService.remove_trainer_from_organization(organization, trainer_user)
            return Response({'detail': 'Trainer removed'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def purchase_seats(self, request, pk=None):
        """Purchase additional trainer seats"""
        organization = self.get_object()
        num_seats = request.data.get('num_seats')
        
        if not num_seats:
            return Response({'detail': 'num_seats required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            overage, total_price = OrganizationService.purchase_extra_seats(organization, int(num_seats))
            return Response({
                'seats_purchased': overage.seats_purchased,
                'price_per_seat': float(overage.price_per_seat),
                'total_price': float(total_price)
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def upgrade_plan(self, request, pk=None):
        """Upgrade organization to a different plan"""
        organization = self.get_object()
        plan_key = request.data.get('plan_key')
        
        if not plan_key:
            return Response({'detail': 'plan_key required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            org = OrganizationService.upgrade_organization_plan(organization, plan_key)
            serializer = self.get_serializer(org)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationInvitationViewSet(viewsets.ViewSet):
    """Manage organization invitations"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def accept_invitation(self, request):
        """Accept an organization invitation"""
        token = request.data.get('token')
        
        if not token:
            return Response({'detail': 'token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invitation = OrganizationService.accept_invitation(token, request.user)
            serializer = OrganizationInvitationSerializer(invitation)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_invitations(self, request):
        """Get current user's pending invitations"""
        invitations = OrganizationInvitation.objects.filter(
            email=request.user.email,
            accepted=False
        )
        serializer = OrganizationInvitationSerializer(invitations, many=True)
        return Response(serializer.data)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Invoice management"""
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    
    def get_queryset(self):
        """Users see only their invoices"""
        from django.db.models import Q
        return Invoice.objects.filter(
            Q(trainer_subscription__trainer=self.request.user) |
            Q(organization__owner=self.request.user)
        )
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download invoice as PDF"""
        invoice = self.get_object()
        # TODO: Implement PDF generation
        return Response({'detail': 'PDF generation coming soon'}, status=status.HTTP_501_NOT_IMPLEMENTED)
