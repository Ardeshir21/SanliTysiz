from django.urls import path
from . import views

app_name = 'baseApp'

# sitemaps_dict = {'Static_sitemap': sitemaps.StaticSitemap,
#                 'Asset_sitemap': sitemaps.AssetSitemap,
#                 'AssetFa_sitemap': sitemaps.AssetFaSitemap,
#                 }
#
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('properties/', views.AssetFilterView.as_view(), name='properties'),
    # path('properties/<int:pk>/', views.AssetSingleView.as_view(), name='propertyView'),
    # path('about-us/', views.ContactView.as_view(), name='about_us'),
    #
    # # This is for sitemap.xml
    # path('RealSiteMap.xml', sitemap, {'sitemaps': sitemaps_dict},
    #  name='django.contrib.sitemaps.views.sitemap'),
]
#
#
# handler404 = 'apps.baseApp.views.error_404'
# handler500 = 'apps.baseApp.views.error_500'
