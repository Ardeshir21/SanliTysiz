from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from . import models, forms, Instagram_Downloader_Login
from apps.baseApp.Instagram_Downloader_Login import crawler
from  urllib.request import urlretrieve
import os
import pickle
from django.conf import settings
from urllib.parse import urlparse



# Here is the Extra Context ditionary which is used in get_context_data of Views classes
def get_extra_context():
    extraContext = {
        'categories': models.Product_Category.objects.all()
        }
    return extraContext


# Index View
class IndexView(generic.TemplateView):
    template_name = 'baseApp/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        context['featured_products'] = models.Product.objects.filter(featured=True, status=True)
        return context

class CategoryListView(generic.ListView):
    context_object_name = 'categories'
    model = models.Product_Category
    template_name = 'baseApp/categories.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        context['page_title'] = 'All Categories'
        context['page_url_detector'] = 'one level depth url'
        return context

class ProductListView(generic.ListView):
    context_object_name = 'products'
    model = models.Product_Category
    template_name = 'baseApp/products.html'

    def get_queryset(self, **kwargs):
        current_category = super(ProductListView, self).get_queryset()
        # Extract current category Object
        current_category = current_category.get(slug=self.kwargs['category'])

        # Extract all products related to current cateory using the categories related_name
        result= current_category.categories.filter(status=True).order_by('-updated')
        return result

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        # We have to extract the Current Category again, because the get_queryset() returns the products list.
        current_category = models.Product_Category.objects.get(slug=self.kwargs['category'])
        context['page_title'] = current_category.name
        context['page_slug'] = self.kwargs['category']
        context['page_url_detector'] = 'two level depth url'
        # Banner Image is showed according to the Category
        context['banner'] = current_category.image_banner
        return context

class ProductDetailView(generic.DetailView):
    context_object_name = 'product'
    model = models.Product
    template_name = 'baseApp/product-details.html'

    def get_object(self, **kwargs):
        singleResult = self.model.objects.get(slug=self.kwargs['product'], status=True)
        # To implement save method on the model which adds view count
        # singleResult.save()
        return singleResult

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        # This returns __str__ of the object
        context['page_title'] = self.get_object()
        context['page_slug'] = self.kwargs['product']
        context['page_url_detector'] = 'three level depth url'
        context['products'] = models.Product.objects.filter(category__slug=self.kwargs['category'], status=True).exclude(slug=self.kwargs['product'])
        context['banner'] = self.get_object().category.image_banner
        return context

# Contact Us
class ContactView(generic.edit.FormView):
    template_name = 'baseApp/contact.html'
    form_class = forms.ContactForm
    success_url = reverse_lazy('baseApp:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # Anotehr way:    current_url = resolve(request.path_info).url_name
        # form.send_email(current_url=self.request.build_absolute_uri())
        form.save()
        return super().form_valid(form)

    # This method calls get_form() and adds the result to the context data with the name ‘form’.
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        # This returns __str__ of the object
        # context['page_title'] = self.get_object()
        # context['page_slug'] = self.kwargs['product']
        # context['page_url_detector'] = 'three level depth url'
        # context['products'] = models.Product.objects.filter(category__slug=self.kwargs['category'], status=True).exclude(slug=self.kwargs['product'])
        # context['banner'] = self.get_object().category.image_banner
        return context

# ABOUT View
class AboutView(generic.TemplateView):
    template_name = 'baseApp/about-us.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        context['featured_products'] = models.Product.objects.filter(featured=True, status=True)
        return context


# TEST View
class TestView(generic.TemplateView):
    template_name = 'baseApp/test.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())
        context['featured_products'] = models.Product.objects.filter(featured=True, status=True)
        return context

# AJAX call which is used to scrape product with URL by client
class AJAX_SCRAPE(generic.TemplateView):
    template_name = 'baseApp/ajax_result.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Append shared extraContext
        context.update(get_extra_context())

        # Get the URL from Instagram
        requested_url = self.request.GET.get('requested_url')

        # while True:
        #     # import saved crawler object
        #     crawler_file_path = os.path.join(settings.MEDIA_ROOT, 'Crawlers\\', 'crawler.pickle')
        #     try:
        #         crawler_obj = open(crawler_file_path, 'rb')
        #         loaded_crawler = pickle.load(crawler_obj)
        #     except FileNotFoundError:
        #         loaded_crawler = False
        #         pass
        #     if loaded_crawler:
        #         break
            # if no crawler object exist, make one instance
        new_crawler= Instagram_Downloader_Login.crawler()
        new_crawler.insta_login()
        # new_crawler.save_crawler()
        # Use the loaded crawler
        # media_addresses = loaded_crawler.list_media_addresses(required_url=requested_url)
        # videos_list = []
        # images_list = []
        #
        # # Download all the files into the Server
        # url_path = urlparse(requested_url).path
        # url_path = url_path.replace('/', '_')
        #
        # # Vidoes
        # for index, file in enumerate(media_addresses['videos_addresses'], start=1):
        #     file_name = '{}_{}.mp4'.format(url_path, index)
        #     temp_file_path = os.path.join(settings.MEDIA_ROOT, 'Downloads\\', file_name)
        #     urlretrieve(file, temp_file_path)
        #     # add file name to the list
        #     videos_list.append(file_name)
        # # Images
        # for index, file in enumerate(media_addresses['images_addresses'], start=1):
        #     file_name = '{}_{}.jpg'.format(url_path, index)
        #     temp_file_path = os.path.join(settings.MEDIA_ROOT, 'Downloads\\', file_name)
        #     urlretrieve(file, temp_file_path)
        #     # add file name to the list
        #     images_list.append(file_name)
        #
        # # CHECK IF this if is needed###################################
        # if loaded_crawler:
        #     context['videos_names'] = videos_list
        #     context['images_names'] = images_list
        # else:
        #     context['videos_names'] = False
        #     context['images_names'] = False
        #
        # context['RequestedLink'] = requested_url
        context['AAA'] = os.path.join(settings.MEDIA_ROOT, 'Crawlers\\', 'crawler.pickle')
        return context

def Download(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'Downloads\\', file_name)
    if file_path.endswith('.mp4'):
        file_type = "video/mp4"
    else:
        file_type = "image/jpeg"

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh, content_type = file_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
