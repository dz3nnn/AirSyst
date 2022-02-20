from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    # Header
    path('about/', views.about),
    path('projects/', views.projects),
    path('certificates/', views.certificates),
    path('contacts/', views.contacts),

    path('cart/', views.cart),
    path('order/', views.order),

    # ??
    path('service_center/', views.service_center),
    path('air_treatment/', views.air_treatment),
    path('catalog/', views.catalog),
    path('equipment/', views.equipment),
    path('product_card/', views.product_card),
    path('project_single/', views.project_single),
    path('reviews/', views.reviews),
    path('spare_parts_next/', views.spare_parts_next),
    path('spare_parts_single/', views.spare_parts_single),
    path('spare_parts/', views.spare_parts),
]
