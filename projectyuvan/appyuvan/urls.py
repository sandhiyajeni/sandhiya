from django.urls import include, path
from appyuvan import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('cart/',views.cart),
    path('login/',views.user_login),
    path('register/',views.register),
    path('logout/',views.user_logout),
    path('catfilter/<a>',views.catfilter),
    path('range/',views.range),
    path('sort/<a>',views.sort),
    path('product_detail/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('qty/<a>/<pid>',views.cartqty),
    path('placeorder/',views.placeorder),
    path('pay/',views.makepayment)
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
