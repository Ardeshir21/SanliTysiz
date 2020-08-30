from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views, sitemaps

app_name = 'baseApp'

sitemaps_dict = {'Static_sitemap': sitemaps.StaticSitemap,
                'Product_sitemap': sitemaps.ProductSitemap,
                'Product_Category_sitemap': sitemaps.Product_CategorySitemap,
                }

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<slug:category>/', views.ProductListView.as_view(), name='products'),
    path('categories/<slug:category>/<slug:product>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('contact/', views.ContactView.as_view(), name='contact-us'),
    path('about/', views.AboutView.as_view(), name='about-us'),

    # This is for sitemap.xml
    path('SanliSiteMap.xml', sitemap, {'sitemaps': sitemaps_dict},
     name='django.contrib.sitemaps.views.sitemap'),
]
#
#
# handler404 = 'apps.baseApp.views.error_404'
# handler500 = 'apps.baseApp.views.error_500'
