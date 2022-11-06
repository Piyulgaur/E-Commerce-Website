"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from craft.views import  cart,profile, index, registration,editAccount,checkout,logout,deleteCart,myOrder
from craft.views import product_desc, saveOrder,shop,login,deleteOrder,compare
from craftAdmins.views import adminLogin,adminProduct,deleteCat,confirmDelivery ,addCategory ,editCategory ,addProduct,editProduct
from craftAdmins.views import adminRegister,adminProfile,editAdminAccount,deleteProduct,adminOrder
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='homepage'),
    path('product/',product_desc),
    path('registration/',registration),
    path('login/',login,name='login'),
    path('logout/',logout),
    path('shop/',shop,name='shop'),
    path('order/',myOrder,name='order'),
    path('compare/',compare),
    path('delete_cart/',deleteCart),
    path('delete_order/',deleteOrder),
    path('cart/',cart,name='cart'),
    path('delivered/',confirmDelivery),
    path('profile/',profile,name='profile'),
    path('edit/',editAccount,name='edit'),
    path('checkout/',checkout),
    path('place_order/',saveOrder),
    path('admin_login/',adminLogin,name='adminLogin'),
    path('admin_register/',adminRegister),
    path('admin_profile/',adminProfile,name='Adminprofile'),
    path('edit_admin_profile/',editAdminAccount),
    path('admin_order/',adminOrder,name='adminOrder'),
    path('admin_product/',adminProduct,name='adminProduct'),
    path('add_product/',addProduct),
    path('add_category/',addCategory),
    path('edit_category/',editCategory),
    path('delete_product/',deleteProduct),
    path('delete_category/',deleteCat),
    path('edit_product/',editProduct,name='editProduct'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


