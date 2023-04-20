from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator


# get user model
User = get_user_model()

# Create your models here.
class Province(models.Model):
    province_name = models.CharField(verbose_name="Province Name", max_length=100, blank=False, unique=True)
    def __str__(self):
        return self.province_name

class District(models.Model):
    province = models.ForeignKey(Province,verbose_name="Province", related_name='districts', on_delete=models.CASCADE)
    district_name = models.CharField(verbose_name="District Name", max_length=100, blank=False, unique=True)
    def __str__(self):
        return self.district_name

class Sector(models.Model):
    district = models.ForeignKey(District,verbose_name="District", related_name='sectors', on_delete=models.CASCADE)
    sector_name = models.CharField(verbose_name="Sector Name", max_length=100, blank=False, unique=True)
    def __str__(self):
        return self.sector_name

class Cell(models.Model):
    sector = models.ForeignKey(Sector,verbose_name="Sector", related_name='cells', on_delete=models.CASCADE)
    cell_name = models.CharField(verbose_name="Cell Name", max_length=100, blank=False, unique=True)
    def __str__(self):
        return self.cell_name

class UserLocation(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name='location', on_delete=models.CASCADE)
    province = models.ForeignKey(Province, verbose_name="Province", on_delete=models.PROTECT, blank=True, null=True)
    district = models.ForeignKey(District, verbose_name="District", on_delete=models.PROTECT, blank=True, null=True)
    sector = models.ForeignKey(Sector, verbose_name="Sector", on_delete=models.PROTECT, blank=True, null=True)
    cell = models.ForeignKey(Cell, verbose_name="Cell", on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)

class Manager(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    user = models.OneToOneField(User, verbose_name="User", related_name='manager_profile', on_delete=models.CASCADE)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    phone_number = PhoneNumberField(verbose_name = "Phone Number",blank=True,)
    profile_image = models.ImageField(
        verbose_name="Profile Picture", 
        upload_to='profile', 
        validators=[FileExtensionValidator(['png','jpg','jpeg'])]
    )
    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profile_image))
    image.allow_tags = True
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)


class Landlord(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    user = models.OneToOneField(User, verbose_name="User", related_name='landlord_profile', on_delete=models.CASCADE)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    phone_number = PhoneNumberField(verbose_name = "Phone Number",blank=True,)
    profile_image = models.ImageField(
        verbose_name="Profile Picture", 
        upload_to='profile', 
        validators=[FileExtensionValidator(['png','jpg','jpeg'])]
    )
    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profile_image))
    image.allow_tags = True
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)


class PropertyType(models.Model):
    type_name = models.CharField(verbose_name="Property Type", max_length=100, unique=True)
    def __str__(self):
        return self.type_name

class Property(models.Model):
    landlord = models.ForeignKey(Landlord, verbose_name="Landlord", related_name='properties', on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, verbose_name="Property Type", related_name='properties', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Property Title", max_length=100)
    description = models.TextField(verbose_name="Property Description", blank=False)
    bedrooms = models.PositiveIntegerField(verbose_name="Bedrooms")
    bathrooms = models.PositiveIntegerField(verbose_name="Bathrooms")
    is_furnished = models.BooleanField(verbose_name="Is furnished", default=False)
    floors = models.PositiveIntegerField(verbose_name="Floors", null=True)
    plot_size = models.TextField(verbose_name="Plot Size")
    renting_price = models.DecimalField(verbose_name="Renting Price", max_digits=10, decimal_places=2)
    status = models.BooleanField(verbose_name="Available", default=True)
    province = models.ForeignKey(Province, verbose_name="Province", on_delete=models.PROTECT)
    district = models.ForeignKey(District, verbose_name="District", on_delete=models.PROTECT)
    sector = models.ForeignKey(Sector, verbose_name="Sector", on_delete=models.PROTECT)
    cell = models.ForeignKey(Cell, verbose_name="Cell", on_delete=models.PROTECT)
    street = models.CharField(verbose_name="Street Address", max_length=50, blank=False)
    pub_date = models.DateTimeField(verbose_name="Published Date", auto_now=True)
    created_date = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    def __str__(self):
        return self.title

class PropertyImages(models.Model):
    property = models.ForeignKey(Property, verbose_name="Property", related_name='images', on_delete=models.CASCADE)
    property_image = models.ImageField(
        verbose_name="Property Image",
        upload_to='properties',
        validators=[FileExtensionValidator(['png','jpg','jpeg'])]
    )
    def rental_image(self):
        return mark_safe('<img src="/../../media/%s" width="120" />' % (self.property_image))
    rental_image.allow_tags = True
    def __str__(self):
        return '{} {}'.format(self.property, self.property_image)

class PublishingPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]
    property = models.ForeignKey(Property, verbose_name="Property", related_name='payments', on_delete=models.PROTECT)
    landlord = models.ForeignKey(Landlord, verbose_name="Landlord", on_delete=models.PROTECT)
    payment_amount = models.DecimalField(verbose_name="Payment Amount", max_digits=10, decimal_places=2)
    payment_method = models.CharField(verbose_name="Payment Method", max_length=50, choices=PAYMENT_METHOD_CHOICES)
    created_date = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    class Meta:
        verbose_name_plural = "Publishing Payments"
    def __str__(self):
        return f"{self.property.title} - {self.landlord.user.first_name} - {self.payment_amount}"

class GetInTouch(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=50, null=False, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, null=False, blank=False)
    email = models.EmailField(verbose_name="Email", max_length=100, null=False, blank=False)
    subject = models.CharField(verbose_name="Subject", max_length=100, null=False, blank=False)
    message = models.TextField(verbose_name="Message", null=False, blank=False)
    is_read = models.BooleanField(verbose_name="Is Read", default=False)
    created_date = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Testimonial(models.Model):
    full_name = models.CharField(verbose_name="Full Name", max_length=100, null=False, blank=False)
    rating = models.IntegerField(verbose_name="Rating Stars", default=0)
    message = models.TextField(verbose_name="Message", null=False, blank=False)
    is_confirmed = models.BooleanField(verbose_name="Confirmed", default=False)
    created_date = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    def __str__(self):
        return self.full_name