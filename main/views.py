from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseRedirect
from .models import Banner,Category,Brand,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from .forms import SignupForm,ReviewAdd,AddressBookForm,ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

# Home Page
def home(request):
    banners = Banner.objects.all().order_by('-id')
    products = Product.objects.filter(is_featured=True).order_by('-id')
    products_with_ratings = []
    for product in products:
        avg_rating = product.get_average_rating()
        products_with_ratings.append((product, avg_rating))
    return render(request, 'index.html', {'products': products_with_ratings, 'banners': banners})


# Category
def category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request,'category_list.html', {'data':data})

# Brand
def brand_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html', {'data':data})

# Product List
def product_list(request):
    total_data = Product.objects.count()
    products = Product.objects.all().order_by('-id')[:3]
    min_price = ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))
    products_with_ratings = []
    for product in products:
        avg_rating = product.get_average_rating()
        products_with_ratings.append((product, avg_rating))
    
    return render(request,'product_list.html',
        {
            'products': products_with_ratings,
            'total_data': total_data,
            'min_price': min_price,
            'max_price': max_price
        }
        )
    
# Product List According to Category
def category_product_list(request,cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')
    products_with_ratings = []
    for product in data:
        avg_rating = product.get_average_rating()
        products_with_ratings.append((product, avg_rating))
    return render(request,'category_product_list.html',
        {
            'products': products_with_ratings,
        }
        )
 
# Product List According to Brand
def brand_product_list(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    products_with_ratings = []
    for product in data:
        avg_rating = product.get_average_rating()
        products_with_ratings.append((product, avg_rating))
    return render(request,'brand_product_list.html',
        {
            'products': products_with_ratings,
        }
        )

# Product Detail
@login_required(login_url='login')  # add this decorator to check if user is authenticated
def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    reviewForm = ReviewAdd()
    
    # Check
    canAdd = True
    reviewCheck = ProductReview.objects.filter(user=request.user,product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # End
    
    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    #End
    
    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    if avg_reviews['avg_rating'] is None:
        avg_reviews['avg_rating'] = 0
	# End
    return render(request, 'product_detail.html',{'data':product, 'related':related_products, 'colors': colors,'reviewForm': reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

# Search
def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'search.html', {'data':data})

# Filter Data
def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(colors)>0:
        allProducts = allProducts.filter(productattribute__color__id__in=colors).distinct()
    if len(categories)>0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
        
    products_with_ratings = []
    for product in allProducts:
        avg_rating = product.get_average_rating()
        products_with_ratings.append((product, avg_rating))
    context = {
        'is_authenticated': request.user.is_authenticated,
        'products': products_with_ratings
    }
    t = render_to_string('ajax/product-list.html',context)
    
    return JsonResponse({'data':t})

def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(colors)>0:
        allProducts = allProducts.filter(productattribute__color__id__in=colors).distinct()
    if len(categories)>0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
        
    products_with_ratings = []
    for product in allProducts:
        avg_rating = product.get_average_rating()
        products_with_ratings.append((product, avg_rating))
    context = {
        'is_authenticated': request.user.is_authenticated,
        'products': products_with_ratings[offset:offset+limit]
    }
    t = render_to_string('ajax/product-list.html',context)
    return JsonResponse({'data':t})


# Add to cart
def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[request.GET['id']] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price']
    }
    
    if 'cartdata' in request.session:
        if request.GET['id'] in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[request.GET['id']]['qty'] = cart_p[request.GET['id']]['qty']
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p 
    return JsonResponse({'data': request.session['cartdata'], 'totalitems':len(request.session['cartdata'])})

# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt += int(item['qty']) * float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})

# Delete Cart Item
def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del cart_data[p_id]
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
            
    t = render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t, 'totalitems':len(request.session['cartdata'])})

# Update Cart Item
def update_cart_item(request):
	p_id=request.GET['id']
	p_qty=request.GET['qty']
 
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[request.GET['id']]['qty']=p_qty
			request.session['cartdata']=cart_data
   
	total_amt=0
 
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
  
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})

	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# SignUp
def signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
        
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html' # Replace with your own login template

    def form_valid(self, form):
        # Call the parent class's form_valid() method to log the user in
        response = super().form_valid(form)

        # Check if the user is an admin
        if self.request.user.is_superuser:
            # Redirect the user to the admin page
            return redirect('admin:index')
        else:
            # Redirect the user to the homepage
            return redirect('home')

# Checkout
@login_required
def checkout(request):
    total_amt=0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            totalAmt += int(item['qty']) * float(item['price'])
        
        # Order
        order = CartOrder.objects.create(
            user = request.user,
            total_amt = totalAmt
        )
        # End
        
        for p_id,item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
            
            # OrderItems
            items=CartOrderItems.objects.create(
				order=order,
				order_no='Order-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
            # End
            
        address = UserAddressBook.objects.filter(user=request.user,status=True).first()
        
        return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'address':address,'order':order})
    
# Save Review
def save_review(request,pid):
    product=Product.objects.get(pk=pid)
    user=request.user
    review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
    data = {
        'user':user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }
    
    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End
    return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# User Dashboard
import calendar
def my_dashboard(request):
    if request.user.is_authenticated:
        orders=CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
        monthNumber=[]
        totalOrders=[]
        for d in orders:
            monthNumber.append(calendar.month_name[d['month']])
            totalOrders.append(d['count'])
        return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(product=product,user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
        product=product,
        user=request.user
        )
        data = {
            'bool': True
        }

    return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html',{'wlist':wlist})

# My Reviews
def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html',{'reviews':reviews})

# My AddressBook
def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})

# Payment
def payment(request):
    del request.session['cartdata']
    
    id = request.GET['id']
    order = CartOrder.objects.get(id=id)
    order.paid_status = True
    order.save()
    
    return render(request, 'index.html')


# Delete from wishlist
def delete_wishlist(request):
    if request.method == "POST":
        item_id = request.POST.get('item-id')
        Wishlist.objects.filter(id=item_id).delete()
        return HttpResponseRedirect(reverse('my_wishlist'))