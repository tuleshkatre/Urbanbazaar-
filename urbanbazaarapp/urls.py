from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from .views import SignupUser , Userlogin , ProductAdd , LogoutView , RedirectView , Customer_dashboard

urlpatterns = [
    path('signup/' , SignupUser.as_view() , name= "signup"),
    path('login/' , Userlogin.as_view() , name= "login"),
    path('product/' , ProductAdd.as_view() , name= "product"),
    path('logout/' , LogoutView.as_view() , name= "logout"),
    path('redirect_view/' , RedirectView.as_view() , name= "redirect_view"),
    path('Customer_dashboard/' , Customer_dashboard.as_view() , name= "Customer_dashboard"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







