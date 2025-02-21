from django.conf import settings
from django.db import models
from django.utils import timezone


class Enquiry(models.Model):
    SERVICE_CHOICES = [
        ('select_service', 'Select Service'),
        ('solar', 'Solar'),
        ('cctv', 'CCTV'),
        ('Network System and Networking', 'Network System and Networking'),
    ]
    
    PREMISES_CHOICES = [
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Retail Store', 'Retail Store'),
        ('Warehouse', 'Warehouse'),
        ('Factory', 'Factory'),
    ]
    
    # Basic Fields
    name = models.CharField(max_length=25)
    phone_number_1 = models.CharField(max_length=10)
    phone_number_2 = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Service Related
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    
    # Conditional Fields for Solar Service
    solar_budget = models.CharField(max_length=100, blank=True, null=True)

    # Conditional Fields for CCTV Service
    premises_type = models.CharField(max_length=50, choices=PREMISES_CHOICES, blank=True, null=True)
    num_cameras = models.IntegerField(blank=True, null=True)
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    installation_address = models.TextField(blank=True, null=True)

    # Additional Comments for Solar and CCTV
    solar_comments = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)  # Correct timezone handling

    def __str__(self):
        return f"Enquiry for {self.name} - {self.service_type}"

# Other models
class Visitor(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Allow null values
    ip_address = models.GenericIPAddressField()
    visit_time = models.DateTimeField(default=timezone.now)  # Default to current time if not provided

    def __str__(self):
        return f"{self.email} - {self.ip_address} - {self.visit_time}"

class CCTVData(models.Model):
    date = models.DateField()  # Ensure there's a date field
    value = models.FloatField() 

    def __str__(self):
        return f"{self.date} - {self.value}"

class SolarData(models.Model):
    date = models.DateTimeField(default=timezone.now)  # Ensure this is a callable default
    value = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.date} - {self.value}"

class WhatsAppenquiry(models.Model):
    date = models.DateTimeField(default=timezone.now)  # Ensure this is a callable default
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.value}"
    
class Carousel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel/')
    button_text = models.CharField(max_length=50, null=True, blank=True)
    button_link = models.URLField(null=True, blank=True)

class Feature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # Store the FontAwesome class
    count = models.PositiveIntegerField()

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    link = models.URLField()

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Index_Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Request(models.Model):
    CATEGORY_CHOICES = [
        ('CCTV', 'CCTV'),
        ('Solar', 'Solar'),
        ('WhatsApp', 'WhatsApp'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)  # Ensure the field name is request_date

    def __str__(self):
        return f'{self.category} request at {self.request_date}'

class contact_enquiry(models.Model):
    SERVICE_CHOICES = [
        ('solar', 'Solar'),
        ('cctv', 'CCTV'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, verbose_name="Full Name", default='')
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=254, verbose_name="Email Address", default='')
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES,
        default='other',
        verbose_name="Service Type"
    )
    additional_comments = models.TextField(blank=True, verbose_name="Additional Comments", default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type.capitalize()}"

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    SERVICE_CHOICES = [
        ('solar', 'Solar'),
        ('cctv', 'CCTV'),
        ('network', 'Network System and Networking'),
    ]
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='solar')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', default="app\static\main\img\Achievement.png")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True)  # Temporarily allow null
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class ComboOffer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name
