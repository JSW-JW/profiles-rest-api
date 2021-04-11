from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10, required=False)

    def validate_name(self, value):
        """Check that the name is starting with 'Mr'"""
        if 'Mr' not in value:
            raise serializers.ValidationError("it's not formatted with 'Mr'. Please keep the rule!")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            password=validated_data.get('password')
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serialize profile feed items"""

    class Meta:
        model=models.ProfileFeedItem
        fields=('id', 'user_profile', 'status_text', 'created_on') # id, created_on fields are by default read_only.
        extra_kwargs = {'user_profile': {'read_only': True}}
