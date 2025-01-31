# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for registration (unimplemented)
    
    # path for login
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    path('get_cars', views.get_cars, name ='getcars'),
    path('get_dealers/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path(route='add_review', view=views.add_review, name='add_review'),


    # path for dealer reviews view (unimplemented)

    # path for add a review view (unimplemented)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)