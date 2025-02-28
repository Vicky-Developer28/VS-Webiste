from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('export_requests/', views.export_to_excel, name='export_requests_excel'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('project/', views.project, name='project'),
    path('term/', views.terms, name='term'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product, name='product'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),



    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path("change-password/", views.change_superuser_password, name="change_password"),

    # Dashboard and Admin Pages
    path('upload/', views.upload_project, name='upload_project'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solar_requests/', views.solar_requests_details, name='solar_requests_details'),
    path('cctv_requests/', views.cctv_requests_details, name='cctv_requests_details'),
    path('NETWORK+REQUESTS/', views.network_requests_details, name='network_requests_details'),
    path('delete_network_request/<int:enquiry_id>/', views.delete_network_request, name='delete_network_request'),
    path('delete_all_network_request/', views.delete_all_network_request, name='delete_all_network_request'),
    path('delete_solar_request/<int:enquiry_id>/', views.delete_solar_request, name='delete_solar_request'),
    path('delete_all_solar_request/', views.delete_all_solar_request, name='delete_all_solar_request'),
     path('delete_all_cctv_request/', views.delete_all_cctv_request, name='delete_all_cctv_request'),
    path('delete_cctv_request/<int:enquiry_id>/', views.delete_cctv_request, name='delete_cctv_request'),
    path('admin/projects/', views.project_backend, name='project-be'),  # Backend Project Management (Unlimited)
    path('admin/index-projects/',  views.index_backend, name='index-be'),  # Backend Index Project Management (Max 6)
    path('projects/upload/', views.upload_project, name='add-project'),  # Regular Project Upload
    path('index-projects/upload/',  views.index_upload_project, name='add-index-project'),  # Index Project Upload (Max 6)
    path('projects/delete/<int:id>/',  views.delete_project, name='delete-project'),  # Delete Main Project
    path('Delete+All-Projects/' , views.delete_all_project, name="delete-all-project"),
    path('index-projects/delete/<int:id>/',  views.index_delete_project, name='delete-index-project'),  # Delete Index Project
    path('Delete+All+Projects/' , views.delete_all_index_project, name="delete-all-index-project"),
    path('storage_usage/', views.storage_usage_view, name='storage_usage'),
    path("terms/", views.track_visitor, name="terms"),
    path('visitor-details/', views.visitor_details, name='visitor_details'),

    # Admin Features
    path('profile/', views.profile, name='profile'),
    path('delete_project/<int:id>/', views.delete_project, name='delete_project'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

