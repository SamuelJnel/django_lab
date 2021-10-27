from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('chinchillas/', views.chinchillas_index, name='index'),
    path('chinchillas/<int:chinchilla_id>/', views.chinchillas_details, name='details'),
    path('chinchillas/create/', views.ChinchillaCreate.as_view(), name='chinchillas_create'),
    path('chinchillas/<int:pk>/update/', views.ChinchillaUpdate.as_view(), name='chinchillas_update'),
    path('chinchillas/<int:pk>/delete/', views.ChinchillaDelete.as_view(), name='chinchillas_delete'),
    path('chinchillas/<int:chinchilla_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('chinchillas/<int:chinchilla_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('chinchillas/<int:chinchilla_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('chinchillas/<int:chinchilla_id>/add_photo/', views.add_photo, name='add_photo'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]