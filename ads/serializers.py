from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category
from users. models import User
from users.serializers import LocationSerializer


class AdSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ad


class AdListSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        exclude = ("description",)
        model = Ad


class AdAuthorSerializer(ModelSerializer):
    total_ads = SerializerMethodField()
    locations = LocationSerializer(many=True)

    def get_global_ads(self, obj):
        return obj.ad_set.count()

    class Meta:
        exclude = ("password", "role")
        model = User


class AdDetailSerializer(ModelSerializer):
    author = AdAuthorSerializer()
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        fields = "__all__"
        model = Ad
