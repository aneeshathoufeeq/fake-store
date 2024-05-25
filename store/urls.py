from django.urls import path
from store import views



urlpatterns = [
 
    path('register/',views.User_register.as_view(),name="register"),
    path('login/',views.Userlogin.as_view(),name="signin"),
    path('logout/',views.Userlogout.as_view(),name="logout"),
    path('vregister/',views.Vregisteration.as_view(),name="vreg"),
    path('addcategory/',views.Addcategory.as_view(),name="addcat"),
    path('addproduct/',views.Addproduct.as_view(),name="addproduct"),
    path('vcategory/',views.Category_list.as_view(),name='vcategory'),
    path('vproduct/<int:pk>',views.Product_list.as_view(),name='vproduct'),
    path('uproduct/<int:pk>',views.ProductUpdate.as_view(),name='uproduct'),
    path('productdetail/<int:pk>',views.ProductDetail.as_view(),name='productdetail'),
    path('vcategorydetail/<int:pk>',views.CategoryDetail.as_view(),name='vcatdetl'),
    path('addtocart/<int:pk>',views.AddToCartView.as_view(),name='addtocart'),
    path('deletecart/<int:pk>',views.CartDelete.as_view(),name='deletecart'), 
    path('viewcart/',views.CartView.as_view(),name='viewcart'), 
    path('order/<int:pk>',views.OrderView.as_view(),name='order'), 




]
