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
    path(route='get_cars', view=views.get_cars, name ='getcars'),

    # path for dealer reviews view (unimplemented)

    # path for add a review view (unimplemented)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
