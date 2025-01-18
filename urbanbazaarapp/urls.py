from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from .views import (
SignupUser , 
Userlogin , 
ProductAdd , 
LogoutView , 
RedirectView , 
Customer_dashboard , 
Vendor_dashboard , 
Admin_dashboard ,
Add_to_cart ,
View_cart ,
Checkout ,
Update_Order_Status ,
Cart_quantity_manage ,
ProductUpdate , 
User_Pass_Change ,
Order_History ,
User_update
)

urlpatterns = [
    path('signup/' , SignupUser.as_view() , name= "signup"),
    path('login/' , Userlogin.as_view() , name= "login"),
    path('product/' , ProductAdd.as_view() , name= "product"),
    path('logout/' , LogoutView.as_view() , name= "logout"),
    path('redirect_view/' , RedirectView.as_view() , name= "redirect_view"),
    path('Customer_dashboard/' , Customer_dashboard.as_view() , name= "Customer_dashboard"),
    path('Vendor_dashboard/' , Vendor_dashboard.as_view() , name= "Vendor_dashboard"),
    path('Admin_dashboard/' , Admin_dashboard.as_view() , name= "Admin_dashboard"),
    path('Add_to_cart/<int:id>/' , Add_to_cart.as_view() , name= "Add_to_cart"),
    path('View_cart/' , View_cart.as_view() , name= "View_cart"),
    path('Checkout/' , Checkout.as_view() , name= "Checkout"),
    path('Update_Order_Status/<int:id>/' , Update_Order_Status.as_view() , name= "Update_Order_Status"),
    path('Update_cart/<int:id>/' , Cart_quantity_manage.as_view() , name= "Update_cart"),
    path('ProductUpdate/<int:id>/' , ProductUpdate.as_view() , name= "ProductUpdate"),
    path('User_Pass_Change/<int:id>/' , User_Pass_Change.as_view() , name= "User_Pass_Change"),
    path('Order_list/' , Order_History.as_view() , name= "Order_list"),
    path('User_update/<int:id>/' , User_update.as_view() , name= "User_update"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








