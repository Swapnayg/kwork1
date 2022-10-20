"""mainKwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from kworkapp.views import update_seller_offers
from apscheduler.schedulers.background import BackgroundScheduler
from kworkapp.views import update_seller_offers

urlpatterns = [
    path('', include("kworkapp.urls")),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('social_django.urls', namespace='social')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

scheduler = BackgroundScheduler()
scheduler.add_job(update_seller_offers, 'cron', hour='12',minute="29",id='my_job_id',max_instances=1)
scheduler.start()
