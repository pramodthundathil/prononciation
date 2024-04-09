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

]
