from rest_framework.fields import SerializerMethodField, BooleanField, IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category, Selection
from users.models import User
from users.serializers import LocationSerializer


class AdSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ad


class AdCreateSerializer(ModelSerializer):
    is_published = BooleanField(validators=[check_not_true], required=False)
    age = IntegerField(read_only=True)

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


class SelectionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Selection


class SelectionListSerializer(ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = Selection


class SelectionCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field="Username", required=False, read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

    class Meta:
        fields = "__all__"
        model = Selection


class SelectionDetailSerializer(ModelSerializer):
    items = AdSerializer(many=True)
    owner = SlugRelatedField(slug_field="Username", queryset=User.objects.all())

    class Meta:
        fields = "__all__"
        model = Selection
