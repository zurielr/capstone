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
    path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    # path for add a review view
    path(route='add_review', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
