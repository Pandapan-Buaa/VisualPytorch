"""VisualPytorch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from NeuralNetwork import views
from VisualPytorch import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'docs/', include_docs_urls(title="VisualPytorch")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/admin/', admin.site.urls),
    path('api/NeuralNetwork/',include('NeuralNetwork.urls')),
    path('api/journal/',include('journal.urls')),
    path('api/user/',include('user.urls')),
    path('api/market/', include('market.urls')),
    path('api/inference/',include('Inference.urls')),
    path('api/', include('comments.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)