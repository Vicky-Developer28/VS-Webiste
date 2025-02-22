#Import All Required library's 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Enquiry, Visitor, SolarData, CCTVData, WhatsAppenquiry , Carousel , Project  , Request , Index_Project , Product, Cart, ComboOffer#  models imported form models.py file

from django.http import HttpResponse, JsonResponse , Http404

from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import login as auth_login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages




from django.db.models import Count
from django.db.models.functions import TruncDate

from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.cache import cache

from django.views.decorators.csrf import csrf_protect , csrf_exempt

from django.utils.crypto import get_random_string
from django.utils.timezone import localtime, now

import logging  

import psutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
from datetime import datetime, timedelta

import mysql.connector

import openpyxl
from openpyxl import Workbook

import json

# Logger
logger = logging.getLogger(__name__)

# Public-facing views

logger = logging.getLogger(__name__)

def index(request):
    index_projects = Index_Project.objects.all()  # Ensure 'projects' is always defined
    carousels = Carousel.objects.all()  # Fetch carousels for the template

    if request.method == 'POST' and request.POST.get('service_type'):
        # Get form data
        name = request.POST.get('name')
        phone_number_1 = request.POST.get('phone_number_1')
        phone_number_2 = request.POST.get('phone_number_2', '')
        email = request.POST.get('email')
        service_type = request.POST.get('service_type')
        installation_address = request.POST.get('installation_address')

        try:
            if service_type == 'solar':
                enquiry = Enquiry.objects.create(
                    name=name,
                    phone_number_1=phone_number_1,
                    phone_number_2=phone_number_2,
                    email=email,
                    service_type=service_type,
                    solar_budget=float(request.POST.get('solar_budget', 0) or 0),
                )
            elif service_type == 'cctv':
                enquiry = Enquiry.objects.create(
                    name=name,
                    phone_number_1=phone_number_1,
                    phone_number_2=phone_number_2,
                    email=email,
                    service_type=service_type,
                    installation_address=installation_address,
                    premises_type=request.POST.get('premises_type', ''),
                    num_cameras=request.POST.get('num_cameras', ''),
                    budget_range=request.POST.get('budget_range', ''),
                )
            
            enquiry.save()  # Save enquiry
            messages.success(request, f"Your {service_type.upper()} enquiry has been submitted successfully!")
            return redirect('index')

        except Exception as e:
            logger.error(f"Error saving {service_type} enquiry: {e}")
            messages.error(request, "There was an error submitting your enquiry. Please try again.")

    return render(request, 'main/index.html', {'carousels': carousels, 'index_projects': index_projects})

def about(request):
    return render(request, 'main/about.html')

def service(request):
    return render(request, 'main/service.html')

def project(request):
    projects = Project.objects.all()
    
    return render(request, 'main//project.html',{'projects': projects})




def contact(request):
    if request.method == 'POST':
        service_type = request.POST.get('service_type', '').strip()

        if not service_type:
            messages.error(request, "Please select a valid service type.")
            return render(request, 'main/contact.html')

        # Common fields
        name = request.POST.get('name', '').strip()
        phone_number_1 = request.POST.get('phone_number_1', '').strip()
        phone_number_2 = request.POST.get('phone_number_2', '').strip()
        email = request.POST.get('email', '').strip()
        installation_address = request.POST.get('installation_address', '').strip()

        try:
            if service_type == 'solar':
                # Solar-specific data
                solar_details = request.POST.get('solar_details', '').strip()
                panel_type = request.POST.get('panel_type', '').strip()
                roof_type = request.POST.get('roof_type', '').strip()
                system_size = float(request.POST.get('system_size', 0) or 0)
                energy_consumption = float(request.POST.get('energy_consumption', 0) or 0)
                solar_budget = float(request.POST.get('solar_budget', 0) or 0)
                site_assessment = 'site_assessment' in request.POST
                financing_options = 'financing_options' in request.POST
                installation_preference = request.POST.get('installation_preference', 'not_decide').strip()
                solar_comments = request.POST.get('solar_comments', '').strip()

                # Save Solar Enquiry
                Enquiry.objects.create(
                    name=name,
                    phone_number_1=phone_number_1,
                    phone_number_2=phone_number_2,
                    email=email,
                    service_type=service_type,
                    installation_address=installation_address,
                    solar_details=solar_details,
                    panel_type=panel_type,
                    roof_type=roof_type,
                    system_size=system_size,
                    energy_consumption=energy_consumption,
                    solar_budget=solar_budget,
                    site_assessment=site_assessment,
                    financing_options=financing_options,
                    installation_preference=installation_preference,
                    additional_comments=solar_comments,
                )
                messages.success(request, "Your solar enquiry has been submitted successfully!")
            elif service_type == 'cctv':
                # CCTV-specific data
                cctv_details = request.POST.get('cctv_details', '').strip()
                premises_type = request.POST.get('premises_type', '').strip()
                num_cameras = request.POST.get('num_cameras', '').strip()
                budget_range = request.POST.get('budget_range', '').strip()

                # Save CCTV Enquiry
                Enquiry.objects.create(
                    name=name,
                    phone_number_1=phone_number_1,
                    phone_number_2=phone_number_2,
                    email=email,
                    service_type=service_type,
                    installation_address=installation_address,
                    premises_type=premises_type,
                    num_cameras=num_cameras,
                    budget_range=budget_range,
                    additional_comments=cctv_details,
                )
                messages.success(request, "Your CCTV enquiry has been submitted successfully!")
            else:
                messages.error(request, "Invalid service type selected.")
                return render(request, 'main/contact.html')

            return redirect('contact')
        except Exception as e:
            logger.error(f"Error saving enquiry: {e}")
            messages.error(request, "There was an error submitting your enquiry. Please try again.")
            return render(request, 'main/contact.html')

    # Handle GET request
    return render(request, 'main/contact.html')


from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Cart, ComboOffer, Category

def product(request):
    products = Product.objects.all()
    cart_items = Cart.objects.all()
    categories = Category.objects.all()

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__name=category_filter)

    return render(request, 'main/products.html', {
        'products': products,
        'cart_items': cart_items,
        'categories': categories
    })

def manage_products(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        try:
            price = Decimal(price)
        except InvalidOperation:
            messages.error(request, "Invalid price. Please enter a valid number.")
            return redirect('manage_products')

        Product.objects.create(name=name, description=description, price=price, image=image)
        messages.success(request, "Product added successfully!")
        return redirect('manage_products')

    products = Product.objects.all()
    combo_offers = ComboOffer.objects.all()
    return render(request, 'admin/products.html', {'products': products, 'combo_offers': combo_offers})

def add_to_cart(request, product_id):
    session_key = request.session.session_key or request.session.create()
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(session_key=session_key, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({'status': 'success', 'message': f'Added {product.name} to cart.'})

def view_cart(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)
    return render(request, 'cart.html', {'cart_items': cart_items})



def terms(request):
    return render(request, 'terms.html')

# User Page Functions




# Back-end Admin pages 
def dashboard(request):
    if not request.user.is_staff:
        return redirect("login")

    # Generate disk usage chart and stats
    chart_data, used, free, total, mysql_used, mysql_total = generate_disk_usage_chart()
    enquiry_chart = generate_request_bar_chart()

    # Time calculations for last 7 days comparison
    current_time = now()
    seven_days_ago = current_time - timedelta(days=7)

    # Enquiry counts for the last 7 days comparison
    solar_requests = Enquiry.objects.filter(service_type='solar').count()
    cctv_requests = Enquiry.objects.filter(service_type='cctv').count()
    total_visitors = Visitor.objects.count()

    # Last 7 days comparison
    solar_last_week = Enquiry.objects.filter(service_type='solar', timestamp__range=[seven_days_ago, current_time]).count()
    cctv_last_week = Enquiry.objects.filter(service_type='cctv', timestamp__range=[seven_days_ago, current_time]).count()
    visitors_last_week = Visitor.objects.filter(visit_time__range=[seven_days_ago, current_time]).count()

    # Calculate percentage changes
    solar_change = calculate_percentage_change(solar_requests, solar_last_week)
    cctv_change = calculate_percentage_change(cctv_requests, cctv_last_week)
    visitor_change = calculate_percentage_change(total_visitors, visitors_last_week)

    context = {
        'user': request.user,
        'solar_requests': solar_requests,
        'cctv_requests': cctv_requests,
        'total_visitors': total_visitors,
        'solar_change': solar_change,
        'cctv_change': cctv_change,
        'visitor_change': visitor_change,
        'chart_data': chart_data,
        'enquiry_chart': enquiry_chart,
        'disk_used': round(used, 2),
        'disk_free': round(free, 2),
        'disk_total': round(total, 2),
        'mysql_used': mysql_used,
        'mysql_total': mysql_total,
        'percent': round((used / total) * 100, 2) if total > 0 else 0,
    }

    return render(request, 'admin/dashboard.html', context)

# Solar Request Page 
@login_required
def solar_requests_details(request):
    refresh = request.GET.get('refresh', False)

    if refresh:
        # If refresh condition is True, redirect to the same URL
        return redirect('solar_requests_details')

    solar_requests = Enquiry.objects.filter(service_type='solar')
    type = 'solar'
    return render(request, 'admin/solar_requests_details.html', {'solar_requests': solar_requests, 'type': type})

# Delete Function for Solar request
@login_required
def delete_solar_request(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id, service_type='solar')
    enquiry.delete()
    messages.success(request, 'Enquiry deleted successfully.')
    return redirect('solar_requests_details')

# CCTV Request Page 
@login_required
def cctv_requests_details(request):
    cctv_requests = Enquiry.objects.filter(service_type='cctv')
    return render(request, 'admin/cctv_requests_details.html', {'cctv_requests': cctv_requests})

# Delete Function for CCTV request
@login_required
def delete_cctv_request(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id, service_type='cctv')
    enquiry.delete()
    messages.success(request, 'Enquiry deleted successfully.')
    return redirect('cctv_requests_details')

# Networking Request Page 

# Convert the Data into Excel File
def export_to_excel(request):
    # Determine the enquiry type based on a query parameter or other logic
    enquiry_type = request.GET.get('type')  # Expecting 'solar' or 'cctv' from the request

    # Validate the enquiry type
    if enquiry_type not in ['solar', 'cctv']:
        return HttpResponse("Invalid enquiry type. Use 'solar' or 'cctv'.", status=400)

    # Filter data based on enquiry type
    data = Enquiry.objects.filter(service_type=enquiry_type)

    # Define headers dynamically based on enquiry type
    if enquiry_type == 'solar':
        headers = [
            'S no', 'Timestamp', 'Name', 'Phone Number 1', 'Phone Number 2', 'Email',
            'Service Type', 'Installation Address', 'Solar Details',
            'Panel Type', 'Roof Type', 'System Size (kW)', 
            'Energy Consumption (kWh)', 'Solar Budget (Rupee)', 
            'Site Assessment', 'Financing Options', 
            'Installation Preference', 'Solar Comments', 
            'Installation Required', 'Budget Range', 
        ]
    elif enquiry_type == 'cctv':
        headers = [
            'S no ', 'Time', 'Name', 'Phone Number 1', 'Phone Number 2', 'Email',
            'Service Type', 'Installation Address', 'CCTV Details',
            'Premises Type', 'Number of Cameras', 'Camera Type', 
            'Recording Storage', 'Mobile Monitoring', 'On-Site Monitoring', 
            'Remote Access', 'Power Source', 'Existing Network',
            'Installation Required', 'Budget Range',
        ]

    # Create an Excel workbook and add a sheet
    wb = Workbook()
    sheet = wb.active
    sheet.title = f"{enquiry_type.capitalize()} Requests"

    # Add headers to the sheet
    sheet.append(headers)

    # Add data rows to the sheet
    for index, obj in enumerate(data, start=1):
        # Convert timezone-aware datetime to naive (localtime) if necessary
        timestamp = localtime(obj.timestamp).replace(tzinfo=None) if obj.timestamp else None

        if enquiry_type == 'solar':
            row = [
                index, timestamp, obj.name, obj.phone_number_1, obj.phone_number_2,
                obj.email, obj.service_type, obj.installation_address,
                obj.solar_details, obj.panel_type, obj.roof_type,
                obj.system_size, obj.energy_consumption, obj.solar_budget,
                obj.site_assessment, obj.financing_options, 
                obj.installation_preference, obj.solar_comments, 
                obj.installation_required, obj.budget_range,
            ]
        elif enquiry_type == 'cctv':
            row = [
                index, timestamp, obj.name, obj.phone_number_1, obj.phone_number_2,
                obj.email, obj.service_type, obj.installation_address,
                obj.cctv_details, obj.premises_type, obj.num_cameras,
                obj.camera_type, obj.recording_storage, obj.mobile_monitoring,
                obj.on_site_monitoring, obj.remote_access, obj.power_source,
                obj.existing_network, obj.installation_required, 
                obj.budget_range,
            ]
        sheet.append(row)

    # Prepare the response to download the file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{enquiry_type}_requests.xlsx"'

    # Save workbook to the response
    wb.save(response)
    return response


# Admin Profile Page
@login_required
def profile(request):
    # Get the current logged-in user
    current_user = request.user
    return render(request, 'admin/profile.html', {'user': current_user})

# Add a Projects in Front-end form Back-End
# Function to Save Projects for Main Projects
def save_project(request):
    """Handles project form submission and saves to the Project database."""
    title = request.POST.get('title')
    category = request.POST.get('category')
    description = request.POST.get('description')
    link = request.POST.get('link')
    image = request.FILES.get('image')

    if not title or not category or not description or not image:
        messages.error(request, "All fields are required.")
        return None  # Indicate failure

    try:
        project = Project(title=title, category=category, description=description, link=link, image=image)
        project.save()
        messages.success(request, "Project uploaded successfully!")
        return project
    except ValidationError as e:
        messages.error(request, f"Error: {e}")
        return None

# Function to Save Projects for Index Page (Limited to 6)
def save_index_project(request):
    """Handles project form submission for Index Page (Max 6 Projects)."""
    if Index_Project.objects.count() >= 6:
        messages.error(request, "6 projects is the maximum limit. If you need more, please contact the developer.")
        return None  # Indicate failure

    title = request.POST.get('title')
    category = request.POST.get('category')
    description = request.POST.get('description')
    link = request.POST.get('link')
    image = request.FILES.get('image')

    if not title or not category or not description or not image:
        messages.error(request, "All fields are required.")
        return None  # Indicate failure

    try:
        project = Index_Project(title=title, category=category, description=description, link=link, image=image)
        project.save()
        messages.success(request, "Index project uploaded successfully!")
        return project
    except ValidationError as e:
        messages.error(request, f"Error: {e}")
        return None

# Backend Project Management (No Limit)
@login_required
def project_backend(request):
    projects = Project.objects.all()
    
    if request.method == 'POST':
        if save_project(request):
            return redirect('project-be')

    return render(request, 'admin/project-backend.html', {'projects': projects})

# Backend Dashboard View (For Index - Limited to 6 Projects)
@login_required
def index_backend(request):
    index_projects = Index_Project.objects.all()[:6]

    if request.method == 'POST':
        if save_index_project(request):
            return redirect('index-be')

    return render(request, 'admin/index-backend.html', {'index_projects': index_projects})

# Frontend Project Upload (Limited to 6 Projects)
@login_required
def index_upload_project(request):
    if request.method == 'POST':
        if save_index_project(request):
            return redirect(request.META.get('HTTP_REFERER', 'index-be'))

    return render(request, 'main/index-project.html')  # Correct template for frontend index projects

# Regular Project Upload (No Limit)
@login_required
def upload_project(request):
    if request.method == 'POST':
        if save_project(request):
            return redirect(request.META.get('HTTP_REFERER', 'project'))

    return render(request, 'main/project.html')  # Correct template for frontend projects

# Delete Main Project
@login_required
def delete_project(request, id):
    project_item = get_object_or_404(Project, id=id)
    project_item.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'project-be'))

# Delete Index Projects (Single or Bulk)
@login_required
def index_delete_project(request, id):  # Ensure 'id' is passed here
    project = get_object_or_404(Index_Project, id=id)
    project.delete()
    return redirect('index-be')  # Redirect after deletion


# ====================================================================================================================================================================================

# Login Function to Admin Page 
def login(request):
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Use the renamed login function
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    return render(request, 'admin/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            if send_otp_email(user, otp):
                messages.success(request, 'OTP sent to your email.')
                return redirect('verify_otp')
            else:
                messages.error(request, 'Failed to send OTP. Try again later.')
        else:
            messages.error(request, 'No user found with this email.')
    return render(request, 'admin/forgot_password.html')

# Generate OTP for Forgot Password
def generate_otp():
    """ Generate a random 6-digit OTP. """
    return get_random_string(length=6, allowed_chars='0123456789ABCDEFGHIJKLMNQRTSOWYXZ')

# Send OTP Mail to Admin Register E-Mail
def send_otp_email(user, otp):
    """Send OTP to the user's email."""
    try:
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}. Please use this to reset your password.',
            'admin@example.com',
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")
        return False


@login_required
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if entered_otp == session_otp:
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'admin/verify_otp.html')

@login_required
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        email = request.session.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('login')
    return render(request, 'admin/reset_password.html')


# Utility functions
def get_client_ip(request):
    """Fetch client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_mysql_storage():
    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="5694",
        database="vimalsolar"
    )
    
    cursor = db_connection.cursor()
    cursor.execute("SHOW TABLE STATUS")

    # Initialize variables for total and used MySQL space
    total_size = 0
    used_size = 0

    for row in cursor.fetchall():
        total_size += row[6]  # 'Data_length' is column 6 in the row
        used_size += row[8]  # 'Index_length' is column 8 in the row

    # Close the connection
    cursor.close()
    db_connection.close()

    # Convert to MB
    total_size_mb = total_size / (1024 * 1024)
    used_size_mb = used_size / (1024 * 1024)

    return used_size_mb, total_size_mb


"""def generate_disk_usage_chart():
    # Get disk usage (for the filesystem)
    disk = psutil.disk_usage('/')
    used = disk.used / (1024 ** 3)  # GB
    free = disk.free / (1024 ** 3)  # GB
    total = disk.total / (1024 ** 3)  # GB

    # Get MySQL storage usage
    mysql_used, mysql_total = get_mysql_storage()

    # Chart labels and data
    labels = ['Used', 'Free']
    sizes = [used, free]
    colors = ['#4CAF50', '#FFC107']

    # Create disk usage pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')

    # Save chart to BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Return disk chart data, MySQL storage, and system storage details
    return chart_data, used, free, total, mysql_used, mysql_total

    buf.close()
    
    return chart_data, used, free, disk.total / (1024 ** 3)"""

def generate_request_bar_chart():
    from django.utils.timezone import now

    # Enquiry data aggregation by date
    today = now().date()
    requests_per_day = Enquiry.objects.annotate(day=TruncDate('timestamp')) \
                                      .values('day') \
                                      .annotate(count=Count('id')) \
                                      .order_by('day')

    # Ensure all days within the last 10 days have data, even if there are no enquiries
    last_7_days = [(today - timedelta(days=i)).strftime('%b %d') for i in range(10, -1, -1)]
    day_count_map = {req['day'].strftime('%b %d'): req['count'] for req in requests_per_day}
    counts = [day_count_map.get(day, 0) for day in last_7_days]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(last_7_days, counts, color='#007bff')

    # Highlight today's enquiries or lack thereof
    if counts[-1] == 0:
        ax.text(6, 0, "No Enquiries Today", fontsize=12, color='red', ha='center')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return chart_data

def calculate_percentage_change(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 2)

def storage_usage_view(request):
    # Get disk usage statistics
    disk = psutil.disk_usage('/')
    total = disk.total / (1024 * 1024 * 1024)  # Convert to GB
    used = disk.used / (1024 * 1024 * 1024)
    free = disk.free / (1024 * 1024 * 1024)
    percent = disk.percent

    # Create pie chart
    labels = ['Used', 'Free']
    sizes = [used, free]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save chart to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_datas = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'admin/storage_usage.html', {'chart_datas': chart_datas, 'total': total, 'used': used, 'free': free, 'percent': percent})


def request_graph_view(request):
    # Fetch the number of requests per day, truncated to date
    requests_per_day = Request.objects.annotate(day=TruncDate('created_at')) \
                                      .values('day', 'category') \
                                      .annotate(count=Count('id')) \
                                      .order_by('day')

    # Data for the graph
    days = [req['day'] for req in requests_per_day]
    categories = list(set(req['category'] for req in requests_per_day))
    counts = {category: [0] * len(days) for category in categories}

    for req in requests_per_day:
        day_index = days.index(req['day'])
        counts[req['category']][day_index] = req['count']

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    for category in categories:
        ax.bar(days, counts[category], label=category)

    # Formatting the chart
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Requests')
    ax.set_title('Requests by Category per Day')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    # Save the chart to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'monitor/request_graph.html', {'chart_data': chart_data})
