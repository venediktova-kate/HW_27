from django.urls import path
from rest_framework import routers

from ads.views import AdViewSet, AdUploadImageView

urlpatterns = [
    path('<int:pk>/upload_image/', AdUploadImageView.as_view()),
]
router = routers. SimpleRouter()
router. register('', AdViewSet)
urlpatterns += router.urls
