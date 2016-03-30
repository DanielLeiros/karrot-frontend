from django.contrib.auth import get_user_model
from yunity.conversations.models import Conversation as ConversationModel
from yunity.groups.models import Group as GroupModel
from rest_framework import serializers


def category(model):
    return {
        'id': model.id,
        'name': model.name,
        'parent': model.parent_id,
    }


def item(model):
    return {
        'id': model.id,
        'user_id': model.user_id,
        'description': model.description,
        'latitude': model.latitude,
        'longitude': model.longitude
    }

def conversation_message(model):
    if model:
        return {
            'id': model.id,
            'sender': model.sent_by_id,
            'created_at': model.created_at.isoformat(),
            'content': model.content,
        }
    else:
        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'display_name', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**{x: validated_data.get(x, None) for x in self.get_fields() if x is not 'id'})


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class meta:
        model = GroupModel
        fields = ['id', 'name', 'description']


def group(model):
    return {
        'id': model.id,
        'name': model.name,
        'description': model.description,
        'members': [user(member) for member in model.hub.members.all()]
    }
class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationModel
        fields = ['id', 'name', 'participants']

