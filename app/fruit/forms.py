from django.forms.models import inlineformset_factory, modelform_factory, modelformset_factory
from django import forms
from .models import Store, Product, Photo, ProductSKU, Sale, Inbox, Vendor, VendorOrder, VendorProduct, Profile
from django.forms import ModelForm
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

import django_filters
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

GeneralWidgets = {
    'startDate': forms.DateInput(format="%d/%m/%Y",attrs={'type': 'text', 'class': 'datepicker'}),
    'address': map_widgets.GoogleMapsAddressWidget,
    'photo': forms.FileInput,
    'sub_total':  forms.TextInput(attrs={'readonly': 'readonly'}),
    'vat': forms.TextInput(attrs={'readonly': 'readonly'}),
    'total': forms.TextInput(attrs={'readonly': 'readonly'}),

}
StoreForm = modelform_factory(
    Store,
    fields="__all__",
    widgets = GeneralWidgets,
    )


ProfileForm = modelform_factory(
    Profile,
    fields=("bio", "location", "facebook", "line_id", "tel", ),
    widgets = GeneralWidgets,
    )

UserForm = modelform_factory(
    User,
    fields=("first_name", "last_name"),
    widgets = GeneralWidgets,
    )

ProductSKUForm = modelform_factory(
    ProductSKU,
    fields="__all__",
    widgets = GeneralWidgets,
    )

ProductForm = modelform_factory(
    Product,
    fields="__all__",
    exclude  = ("store", ),
    widgets = GeneralWidgets,
    )

SaleForm = modelform_factory(
    Sale,
    fields="__all__",
    #exclude  = ("store", ),
    widgets = GeneralWidgets,
    )

InboxForm = modelform_factory(
    Inbox,
    fields="__all__",
    #exclude  = ("store", ),
    widgets = GeneralWidgets,
    )

VendorForm = modelform_factory(
    Vendor,
    fields="__all__",
    exclude  = ("store", ),
    widgets = GeneralWidgets,
    )

VendorProductForm = modelform_factory(
    VendorProduct,
    fields="__all__",
    exclude  = ("store", "vendor"),
    widgets = GeneralWidgets,
    )

VendorOrderForm = modelform_factory(
    VendorOrder,
    fields="__all__",
    exclude  = ("store", ),
    widgets = GeneralWidgets,
    )

PhotoFormSet = modelformset_factory(
    Photo,
    fields="__all__",
    exclude  = ("product", ),
    #extra = 3,
    widgets = GeneralWidgets,
    )

InlinePhotoFormset = inlineformset_factory(Product, Photo,  fields="__all__", widgets= GeneralWidgets)

InlineVendorProductFormset = inlineformset_factory(Vendor, VendorProduct,  fields="__all__", widgets= GeneralWidgets)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'code', 'price']

class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['product', 'sku', 'buyer', 'n_unit', 'unit_name']

class InboxFilter(django_filters.FilterSet):
    class Meta:
        model = Inbox
        fields = ['store', 'product', 'buyer', 'subject', 'body', 'tel', 'status', 'created_at']

class VendorFilter(django_filters.FilterSet):
    class Meta:
        model = Vendor
        fields = ['name', 'code',  'description', 'tel',  'line_id', 'email', 'created_at']

class VendorOrderFilter(django_filters.FilterSet):
    class Meta:
        model = VendorOrder
        fields = ['vendor', 'product', 'store', 'price', 'n_unit',  'unit_name', 'total', 'created_at']



class SignUpForm(UserCreationForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    roles = forms.ChoiceField(choices = (("seller", "Seller"), ("buyer", "Buyer")))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'roles', )


