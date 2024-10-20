from django.urls import path

from .views import(
       user_profile_view
)

app_name= 'profile'
urlpatterns = [
    path('profule/<int:id>/', user_profile_view, name='profile'),   

]
