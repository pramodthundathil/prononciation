from django.urls import path
from .import views 

urlpatterns = [
    path("",views.Index,name="Index"),
    path("Detect",views.Detect,name="Detect"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("AddPrononciation",views.AddPrononciation,name="AddPrononciation"),
    path("AllPrononciations",views.AllPrononciations,name="AllPrononciations"),
    path("Addcomment/<int:pk>",views.Addcomment,name="Addcomment"),
    path("Search",views.Search,name="Search"),
    path("CheckPrononciation",views.CheckPrononciation,name="CheckPrononciation"),
    path("GetPronon",views.GetPronon,name="GetPronon"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),
    path("DeletePronunciation/<int:pk>",views.DeletePronunciation,name="DeletePronunciation"),
    path('like_audio/<int:pk>/', views.like_audio, name='like_audio')


]
