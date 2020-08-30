from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField


# ASSET_TYPES = [('FL', 'Flat'),
#                 ('VI', 'Villa'),
#                 ('OF', 'Office'),
#                 ('ST', 'Store')]

BOOL_STATUS = [(True, 'Active'),
                (False, 'Deactive')]


class Product_Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, allow_unicode=True,
                                help_text="The name of the page as it will appear in URLs e.g http://domain.com/[category-slug]/")
    icon =  models.CharField(max_length=150, unique=True, blank=True, null=True)
    image_thumb = models.ImageField(upload_to='baseApp/categories/', blank=True, null=True,
                                help_text='Thumbnail Image')
    image_banner = models.ImageField(upload_to='baseApp/categories/', blank=True, null=True,
                                help_text='Banner Image')
    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = "Product_Categories"

    def get_absolute_url(self):
        return reverse('baseApp:products', kwargs={'category': self.slug})

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Product_Category, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField(default=0.0)
    width = models.PositiveIntegerField(default=0)
    color = models.ManyToManyField(Color, related_name='colors')
    contry_of_origin = models.CharField(max_length=50, default='Turkey')
    content = RichTextUploadingField(default='Here is the product detailed information')
    content_extra = RichTextUploadingField(default='Here is the product EXTRA information')
    shortContent = models.TextField(max_length=370, blank=True, help_text='Max Characters = 370')
    image_thumb = models.ImageField(upload_to='baseApp/products/', blank=True, null=True,
                                help_text="Thumbnail Image 555x400")
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, allow_unicode=True,
                                help_text="The name of the page as it will appear in URLs e.g http://domain.com/[category-slug]/[product-slug]/")
    created = models.DateField(editable=False)
    updated = models.DateField(editable=False)
    status = models.BooleanField(choices=BOOL_STATUS, default=False)
    featured = models.BooleanField(choices=BOOL_STATUS, default=False,
                                    help_text='Display this item on the Home page')
    # view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('baseApp:product_detail', kwargs={'category': self.category.slug ,
                                                        'product': self.slug})

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='slideshow_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='baseApp/products/', null=True,
                                help_text='Slide Image 750x500')
    display_order = models.PositiveIntegerField(null=True, blank=True)

    class Meta():
        verbose_name_plural = "Product Images"
        ordering = ['display_order']

class ContactUsMessage(models.Model):
    sender_request = models.ManyToManyField(Product, related_name='messages')
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField(max_length=100)
    sender_number = PhoneNumberField(blank=True)
    sender_message = models.TextField(max_length=500)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, set the timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(ContactUsMessage, self).save(*args, **kwargs)
