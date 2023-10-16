from .models import Post
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    # 'owner' as a ReadOnlyField displaying the owner's username
    owner = serializers.ReadOnlyField(source='owner.username')
    
    # 'is_owner' as a SerializerMethodField
    is_owner = serializers.SerializerMethodField()
    
    # 'profile_id' as a ReadOnlyField displaying the owner's profile id
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    
    # 'profile_image' as a ReadOnlyField displaying the owner's profile image url
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')  # Assuming 'image' field on Profile model is an ImageField


    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value
    
    # Define the 'get_is_owner' method
    def get_is_owner(self, obj):
        # Check if the request user is the owner of the post
        return self.context['request'].user == obj.owner

    class Meta:
        model = Post
        fields = ['id', 'owner', 'is_owner', 'profile_id', 'profile_image', 'title', 'content', 'image']  # Assuming 'title' and 'content' are fields on the Post model
