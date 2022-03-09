from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    # Header
    path('about/', views.about, name='about'),
    path('certificates/', views.certificates, name='certificates'),
    path('contacts/', views.contacts, name='contacts'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('reviews/', views.reviews, name='reviews'),
    path('service_center/', views.service_center),

    # Equipment
    path('equipment/', views.equipment, name='equipment'),
    path('equipment/category/<int:category_id>/',
         views.equipment_by_category, name='equipment_by_category'),
    path('equipment/category/catalog/<int:category_id>/',
         views.equipment_catalog_by_category, name='equipment_catalog_by_category'),
    path('equipment/sub_category/catalog/<int:sub_category_id>/',
         views.equipment_catalog_by_sub_category, name='equipment_catalog_by_sub_category'),

    # Single Equipment Page
    path('equipment_single/<int:product_id>/',
         views.equipment_single, name='equipment_single'),

    # Parts
    path('parts/', views.spare_parts, name='parts'),
    path('parts_type/', views.spare_parts_next, name='parts_type'),
    path('parts_single/', views.spare_parts_single, name='parts_single'),

    # Projects
    path('projects/', views.projects, name='projects'),
    path('project/<int:project_id>/', views.project_single, name='project_by_id'),

    #     Send info
    path('send_feedback/', views.send_feedback, name='send_feedback'),
    path('send_basket/', views.send_basket, name='send_basket'),

]
