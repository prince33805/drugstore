from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path('store/', views.store,name="store"),
    path('store/<str:pk_test>/', views.viewProduct,name="view_product"),
    path('store/category/<str:pk_test>/', views.category,name="category"),
    path('cart/', views.cart,name="cart"),
    path('checkout/', views.checkout,name="checkout"),
    
    path('profile/', views.profile,name="profile"),
    path('profile/update', views.profileUpdate,name="profile_update"),
    path('vieworder/<str:pk_test>/', views.cusViewOrder,name="cus_view_order"),
    
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
    path('register/', views.registerPage,name="register"),
    path('login/', views.loginPage,name="login"),
    path('logout/', views.logoutUser,name="logout"),
    
    path('', views.home,name="home"),
    
    path('company/', views.company,name="company"),
    path('company/<str:pk_test>/', views.viewCompany,name="view_company"),
    path('update_company/<str:id>/', views.updateCompany,name="update_company"),
    path('delete_company/<str:id>/',views.deleteCompany,name="delete_company"),
    
    path('employee/', views.employee,name="employee"),
    path('update_employee/<str:id>/', views.updateEmployee,name="update_employee"),
    path('delete_employee/<str:id>/',views.deleteEmployee,name="delete_employee"),
    
    path('medicine/', views.medicine,name="medicine"),
    path('medicine/<str:pk_test>/', views.viewMedicine,name="view_medicine"),
    path('update_medicine/<str:id>/', views.updateMedicine,name="update_medicine"),
    
    path('customer/', views.customer,name="customer"),
    path('customer/<str:pk_test>/', views.customerDetail,name="customer_detail"),
    
    path('order/', views.order,name="order"),
    path('order/<str:pk_test>/', views.viewOrder,name="view_order"),
    
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)