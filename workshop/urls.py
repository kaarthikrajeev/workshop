"""workshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from wrkshopapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('reglog', views.reglog),
    path('registration', views.registration),
    path('adminhome', views.adminhome),
    path('userhome', views.userhome),
    path('techhome', views.techhome),
    path('adminstaff', views.adminstaff),
    path('adminupdatestaff', views.adminupdatestaff),
    path('admindeletestaff', views.admindeletestaff),
    path('viewfeedback', views.viewfeedback),
    path('addfeedback', views.addfeedback),
    path('addrequest', views.addrequest),
    path('viewuserrequests', views.viewuserrequests),
    path('cancelrequest', views.cancelrequest),
    path('viewbookings', views.viewbookings),
    path('schedulebooking', views.schedulebooking),
    path('viewtechschedules', views.viewtechschedules),
    path('viewtechcompleted', views.viewtechcompleted),
    path('addwrkdetails', views.addwrkdetails),
    path('viewwrkdetails', views.viewwrkdetails),
    path('addpayment', views.addpayment),
    

]
