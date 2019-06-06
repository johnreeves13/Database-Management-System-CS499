"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

#This is a file automatically generated my django. We put in urls to get the program to be able to go to different urls when called.

from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/$', "search.views.get_results"),
    url(r'^search/claims_result.html/$', TemplateView.as_view(template_name='claims_result.html')),
    url(r'^search/ppo_result.html/$', TemplateView.as_view(template_name='ppo_result.html')),
    url(r'^search/invoices_result.html/$', TemplateView.as_view(template_name='invoices_result.html')),
    url(r'^search/claims_result.html/$', TemplateView.as_view(template_name='claims_result.html')),
    url(r'^search/total_cost_result.html/$', TemplateView.as_view(template_name='total_cost_result.html')),

]
