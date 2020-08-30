from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.baseApp.models import Product_Category, Product

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ['baseApp:index', 'baseApp:contact-us',
                'baseApp:about-us']

    def location(self, item):
        return reverse(item)

# Product
class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated


# Product_Category
class Product_CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Product_Category.objects.all()
