# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    path('logout/', views.logout_request, name='logout_request'),
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    # path(route='login', view=views.login_user, name='login'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
