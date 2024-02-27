from rest_framework import serializers
from django.contrib.auth import get_user_model
from business.models import Business

User = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    has_completed_onboarding = serializers.SerializerMethodField()

    def get_has_completed_onboarding(self, obj):
        try:
            Business.objects.get(user=obj)
            return True
        except Business.DoesNotExist:
            return False
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'has_completed_onboarding')
        read_only_fields = ('id', 'email')
