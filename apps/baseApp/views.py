from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms



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
