from . import views
from django.urls import path
urlpatterns = [
    path('',views.home,name="home"),
    path('main/',views.main,name="main"),
    path('upload/',views.upload,name="upload"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('logout/',views.logout,name="logout"),
    path('atsadmin/',views.atsadmin,name="atsadmin"),
    path('addskills/',views.addskills,name="addskills"),
    path('add/',views.add,name="add"),
    path('alldata/',views.alldata,name="alldata"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('delete/<str:pk_id>',views.delete,name="delete"),
    path('openstat/<str:pk1_id>',views.openstat,name="openstat"),
    path('output/',views.description,name="description"),
]