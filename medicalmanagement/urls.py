
from django.contrib import admin
from django.urls import path
from medical import views
from django.contrib.auth.views import LogoutView
from django.urls import path,include
from medical.views import *
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('customer/',include('customer.urls')),
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='medical/logout.html'),name='logout'),
    path('aboutus/', views.aboutus_view),
   
    path('logout/', LogoutUser),
    path('loginuser/',LoginUser),
    path('homepage', HomePage),
    path('clicklogin', clicklogin),
    path('register_user/',RegisterUser),
    path('click_user', ClickRegister),
    path('fruits/', fruits),
    path('classification1',classification1),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)