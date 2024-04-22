from rest_framework import serializers
from .models import User,Friendship
import re


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField( write_only=True,required=False,min_length=8, error_messages={
                                            "blank": "Password cannot be empty.",
                                            "min_length": "Password too short.",
                                        },)  
    full_name = serializers.CharField(source='get_full_name', read_only= True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id','username', 'email','password','full_name','first_name','last_name')
        
   # Validation on the password, which contains 1 uppercase, 1 lowercase
    def validate_password(self,value):
        if not re.findall('(?=.*[a-z])(?=.*[A-Z])', value):
            raise serializers.ValidationError("The password must contain at least 1 uppercase, 1 lowercase ")
        return value    
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class FriendshipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'is_accepted', 'created_at']
        read_only_fields = ['from_user']  # Mark from_user and to_user as read-only

    def create(self, validated_data):
        from_user = self.context['request'].user
        friendship = Friendship.objects.create(from_user=from_user,**validated_data)
        return friendship
    
class FriendshipRespondSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Friendship
        fields = ['from_user', 'to_user', 'is_accepted', 'created_at']
        read_only_fields = ['from_user']  # Mark from_user and to_user as read-only

    def validate_is_accepted(self, value):
        if value not in [True,False]:
            raise serializers.ValidationError(
                        "In valid is_accpeted value. it accepts only Boolean"
                    )