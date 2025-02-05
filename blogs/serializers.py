from rest_framework import serializers
from .models import Blog
from .models import Comment

# Serializer for the Blog model
class BlogSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'date', 'image']


# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    blog = serializers.HiddenField(default=None)

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']