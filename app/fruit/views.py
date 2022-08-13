#from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from fruit.models import Store, Product, Photo, ProductSKU, Sale, Inbox, Vendor, VendorProduct

from .forms import StoreForm, ProductForm, InboxForm, SaleForm,  PhotoFormSet,VendorFilter,  InlinePhotoFormset, ProductSKUForm, ProductFilter, SaleFilter, InboxFilter, VendorForm, VendorOrderForm, VendorOrderFilter, VendorOrder, InlineVendorProductFormset, VendorProductForm, SignUpForm, ProfileForm, UserForm
from django.contrib import messages
from django.core.paginator import Paginator

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


from django.contrib.auth.models import User


def index(request):
    return render(request, 'fruit/index.html')



@login_required
def mystore(request):
    stores = request.user.store_created.all().order_by("-created_at")
    products = stores[0].product_set.all().order_by("-created_at")

    if request.method == "POST":
        if 'createStore' in request.POST:
            print("create store")
            name = request.POST.get('name', None)
            store = Store()
            store.name = name
            store.created_by  = request.user
            store.save()

        if 'updateStore' in request.POST:
            print("update store")
            storeForm = StoreForm(request.POST, instance=stores[0])
            if storeForm.is_valid():
                storeForm.save()

        return redirect("fruit:mystore")
            #print("Create Store")
    else:
        storeForm = StoreForm(instance=stores[0])
    #print(dir(request.user))
    return render(request, 'fruit/mystore_index.html', {'stores': stores, 'storeForm': storeForm, 'products': products, 'mystore': True})


@login_required
def product_index(request):
    stores = request.user.store_created.all().order_by("-created_at")
    products = stores[0].product_set.all().order_by("-created_at")

    f = ProductFilter(request.GET, queryset=products)

    paginator = Paginator(f.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fruit/product_index.html', {'products': products, 'product': True, 'page_obj': page_obj, 'filter': f})

@login_required
def sale_index(request):
    stores = request.user.store_created.all().order_by("-created_at")
    o_qs = stores[0].sale_set.all().order_by("-created_at")

    f = SaleFilter(request.GET, queryset=o_qs)

    paginator = Paginator(f.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fruit/sale_index.html', {'o_qs': o_qs, 'sale_active': True, 'page_obj': page_obj, 'filter': f})

@login_required
def create_product(request):
    stores = request.user.store_created.all().order_by("-created_at")
    form = ProductForm()
    form2 = InlinePhotoFormset()
    if request.method == "POST":
        form = ProductForm(request.POST)
        form2 = InlinePhotoFormset(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            instance1 = form.save(commit=False)
            instance1.created_by = request.user
            instance1.store = stores[0]
            instance1.save()
            instances = form2.save(commit=False)
            print(instances)

            for s in instances:
                s.product = instance1
                s.created_by = request.user
                s.save()
            messages.success(request, "Product Save")

        else:
            if form.errors:
                messages.error(request, form.errors)
            if form2.errors:
                messages.error(request, form2.errors)

            print("Invalid ")
        return redirect("fruit:product_edit", pk=int(instance1.id))

    return render(request, 'fruit/product_form.html', {'product': True, 'form': form, 'form2': form2 })

@login_required
def create_sku(request, pk):
    p = Product.objects.get(pk=pk)
    form = ProductSKUForm(initial={'product':p, 'created_by': request.user})
    if request.method == "POST":
        form = ProductSKUForm(request.POST)
        if form.is_valid():
            i = form.save()
            messages.success(request, "Product Save")
            return redirect("fruit:edit_sku", pk=i.pk)
        else:
            messages.error(request, form.errors)
            return redirect("fruit:create_sku", pk=int(pk))

    return render(request, 'fruit/sku_form.html', {'form': form, 'pid': p.pk})

@login_required
def edit_sku(request, pk):

    p = ProductSKU.objects.get(pk=pk)
    p0 = p.product

    form = ProductSKUForm(instance=p)
    if request.method == "POST":
        form = ProductSKUForm(request.POST)
        if form.is_valid():
            i = form.save()
            messages.success(request, "Product Save")
            return redirect("fruit:edit_sku", pk=i.pk)
        else:
            message.error(request, "SKU  created failed")
            return redirect("fruit:create_sku", pk=int(pk))

    return render(request, 'fruit/sku_form.html', {'form': form, 'pid': p0.pk})

@login_required
def product_edit(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")

    product = Product.objects.get(pk=pk)
    form = ProductForm(instance = product)
    form2 = InlinePhotoFormset(instance = product)

    if request.method == "POST":
        form = ProductForm(request.POST)
        form2 = InlinePhotoFormset(request.POST, request.FILES, instance = product)
        if form.is_valid() and form2.is_valid():
            instance1 = form.save(commit=False)
            instance1.created_by = request.user
            instance1.store = stores[0]
            instance1.save()
            instances = form2.save(commit=True)
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Product Save")
        else:
            print("Invalid ")
            print(form.errors)
            print(form2.errors)

            if form.errors:
                messages.error(request, form.errors)
            if form2.errors:
                messages.error(request, form2.errors)

        return redirect("fruit:product_edit", pk =  int(pk))

    return render(request, 'fruit/product_form.html', {'product': True, 'form': form, 'form2': form2, 'obj': product })

@login_required
def sale_edit(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")

    obj = Sale.objects.get(pk=pk)
    form = SaleForm(instance = obj)

    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            instance1 = form.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Sale Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)

        return redirect("fruit:sale_edit", pk =  int(pk))

    return render(request, 'fruit/sale_form.html', {'sale_active': True, 'form': form, 'object': obj})


@login_required
def inbox_index(request):
    stores = request.user.store_created.all().order_by("-created_at")
    o_qs = stores[0].inbox_set.all().order_by("-created_at")

    f = InboxFilter(request.GET, queryset=o_qs)

    paginator = Paginator(f.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fruit/inbox_index.html', {'o_qs': o_qs, 'inbox_active': True, 'page_obj': page_obj, 'filter': f})

@login_required
def inbox_edit(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")

    obj = Inbox.objects.get(pk=pk)
    form = InboxForm(instance = obj)

    if request.method == "POST":
        form = InboxForm(request.POST)
        if form.is_valid():
            instance1 = form.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Sale Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)

        return redirect("fruit:sale_edit", pk =  int(pk))

    return render(request, 'fruit/inbox_form.html', {'inbox_active': True, 'form': form, 'object': obj})

@login_required
def vendor_index(request):
    stores = request.user.store_created.all().order_by("-created_at")
    o_qs = stores[0].vendor_set.all().order_by("-created_at")

    f = VendorFilter(request.GET, queryset=o_qs)

    paginator = Paginator(f.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fruit/vendor_index.html', {'o_qs': o_qs, 'vendor_active': True, 'page_obj': page_obj, 'filter': f})

@login_required
def vendor_edit(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")

    obj = Vendor.objects.get(pk=pk)
    form = VendorForm(instance = obj)
    form2 = InlineVendorProductFormset(instance = obj)
    for f in form2:
        f.fields['product'].queryset = stores[0].product_set.all().order_by("-created_at")

    if request.method == "POST":
        form = VendorForm(request.POST)
        form2 = InlineVendorProductFormset(request.POST, instance = obj)
        if form.is_valid() and form2.is_valid():
            instance1 = form.save()
            instance2 = form2.save(commit=False)

            for i in instance2:
                i.created_by = request.user
                i.save()

            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Vendor Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)
            if form2.errors:
                messages.error(request, form2.errors)

        return redirect("fruit:vendor_edit", pk =  int(pk))

    return render(request, 'fruit/vendor_form.html', {'vendor_active': True, 'form': form, 'obj': obj, 'form2': form2})

@login_required
def vendor_create(request):
    stores = request.user.store_created.all().order_by("-created_at")

    form = VendorForm()

    #form.fields['products'].queryset = stores[0].product_set.all().order_by("-created_at")

    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():

            instance1 = form.save(commit=False)
            instance1.store = stores[0]
            instance1.created_by = request.user
            instance1.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Sale Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)

        return redirect("fruit:vendor_edit", pk =  instance1.pk)

    return render(request, 'fruit/vendor_form.html', {'vendor_active': True, 'form': form})

@login_required
def vendorproduct_create(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")
    print(pk)
    vendor = Vendor.objects.get(pk=pk)

    form = VendorProductForm()

    form.fields['product'].queryset = stores[0].product_set.all().order_by("-created_at")

    if request.method == "POST":
        form = VendorProductForm(request.POST)
        if form.is_valid():

            instance1 = form.save(commit=False)
            instance1.store = stores[0]
            instance1.vendor = vendor
            instance1.created_by = request.user
            instance1.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Sale Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)

        return redirect("fruit:vendorproduct_edit", pk =  instance1.pk)

    return render(request, 'fruit/vendorproduct_form.html', {'vendor_active': True, 'form': form, 'vendor': vendor})

@login_required
def vendorproduct_edit(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")

    obj = VendorProduct.objects.get(pk=pk)
    form = VendorProductForm(instance = obj)
    vendor = obj.vendor

    form.fields['product'].queryset = stores[0].product_set.all().order_by("-created_at")

    if request.method == "POST":
        form = VendorProductForm(request.POST)
        if form.is_valid():
            instance1 = form.save()

            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Vendor Product Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)

        return redirect("fruit:vendorproduct_edit", pk =  int(pk))

    return render(request, 'fruit/vendorproduct_form.html', {'vendor_active': True, 'form': form, 'obj': obj, 'vendor': vendor})

#vendor order
@login_required
def vendororder_index(request):
    stores = request.user.store_created.all().order_by("-created_at")
    o_qs = stores[0].vendororder_set.all().order_by("-created_at")

    f = VendorOrderFilter(request.GET, queryset=o_qs)

    paginator = Paginator(f.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fruit/vendororder_index.html', {'o_qs': o_qs, 'vendor_active': True, 'page_obj': page_obj, 'filter': f})


@login_required
def vendororder_edit(request, pk):
    stores = request.user.store_created.all().order_by("-created_at")

    obj = VendorOrder.objects.get(pk=pk)
    form = VendorOrderForm(instance = obj)
    form.fields['vendor'].queryset = stores[0].vendor_set.all().order_by("-created_at")
    #form.fields['product'].queryset = stores[0].product_set.all().order_by("-created_at")

    if request.method == "POST":
        form = VendorOrderForm(request.POST)
        if form.is_valid():
            instance1 = form.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Sale Save")
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)

        return redirect("fruit:vendororder_edit", pk =  int(pk))

    return render(request, 'fruit/vendororder_form.html', {'vendor_active': True, 'form': form, 'object': obj})

@login_required
def vendororder_create(request):
    stores = request.user.store_created.all().order_by("-created_at")

    form = VendorOrderForm()
    form.fields['vendor'].queryset = stores[0].vendor_set.all().order_by("-created_at")
    #form = stores[0].vendor_set.all()

    if request.method == "POST":
        form = VendorOrderForm(request.POST)
        if form.is_valid():

            instance1 = form.save(commit=False)
            instance1.store = stores[0]
            instance1.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Vendor Order Save")
            return redirect("fruit:vendororder_edit", pk =  instance1.pk)
        else:
            print("Invalid ")
            if form.errors:
                messages.error(request, form.errors)


    return render(request, 'fruit/vendororder_form.html', {'vendororder_active': True, 'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.profile.roles = form.cleaned_data['roles']
            user.profile.save()
            current_site = "https://localhost:8000"
            subject = 'Activate Your MySite Account'
            message = render_to_string('fruit/account_activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('fruit:account_activation_sent')

    else:
        form = SignUpForm()
    return render(request, 'fruit/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('front:index')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, "fruit/account_activation_sent.html")


@login_required
def profile(request):
    form1 = UserForm(instance = request.user)
    user = request.user
    form2 = ProfileForm(instance = request.user.profile)
    if request.method == "POST":
        form1 = UserForm(request.POST, instance=request.user)
        form2 = ProfileForm(request.POST, instance=request.user.profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            '''
            print(instances)
            for s in instances:
                s.product = instance1
                s.save()
            '''
            messages.success(request, "Profile Save")
            return redirect("fruit:profile")
        else:
            print("Invalid ")
            if form1.errors:
                messages.error(request, form1.errors)
            if form2.errors:
                messages.error(request, form2.errors)

    return render(request, 'fruit/profile.html', {'form1': form1, 'form2': form2, 'user': user, 'profile': True} )
