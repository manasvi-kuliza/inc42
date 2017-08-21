from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^company/', views.Company.as_view(), name='company'),
    url(r'^upload-logo/', views.UploadCompanyLogo.as_view(), name='upload-company-logo'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
