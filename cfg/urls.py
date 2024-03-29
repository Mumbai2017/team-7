"""cfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from app import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sms/', views.recieve_sms),
    url(r'^hello/', views.hello_world),
    url(r'^registersakhi/', views.register_sakhi),
    url(r'^registeruser/', views.register_user),    
    url(r'^getlocation/(\d+)/(\d+)/$', views.get_location),
    url(r'^customer-order/$', views.customer_order),
    url(r'^match_order/(\d+)/$', views.match_order),
    url(r'^order_status/(\d+)/$', views.order_status),
    url(r'^login_sakhi/$', views.login_sakhi),
    url(r'^sakhi_dashboard/$', views.sakhi_dashboard),
    url(r'^order_complete/(\d+)/', views.order_complete),
    url(r'^gruh_dashboard_1/', views.gruh_dashboard_1),
    url(r'^gruh_dashboard_2/', views.gruh_dashboard_2),
    url(r'^gruh_dashboard_3/', views.gruh_dashboard_3),
    url(r'^update_inventory/$', views.update_inventory),
    url(r'^login_customer/$', views.login_customer),
    url(r'^cluster/$', views.location_cluster),
]
