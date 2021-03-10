from django.shortcuts import render,HttpResponsePermanentRedirect,redirect,reverse,HttpResponseRedirect
from django.views.generic import DetailView,View,ListView
from .models import Product,Category,Whishlist,User,Tag
from specs.models import ProductFeatures
from django.db.models import Q
# from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib import messages


def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.add_message(request,messages.SUCCESS,'Товар добавлен в избранноe')
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))



def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
    

def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


def cart_detail(request):
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))



class IndexView(View):
    def get(self,request,*args,**kwargs):
        new_item = Product.objects.order_by('-pk')[:4]
        parfumes = Product.objects.filter(category__name='Парфюмерия')[:6]
        probes = Product.objects.filter(category__name='Пробники')[:6]
        accessories = Product.objects.filter(category__name='Аксессуары')[:6]
        title = 'Elena-Shop :: Parfume storage'

        

        context= {
            'title': title ,
            'parfumes' : parfumes,
            'probes':probes,
            'accessories':accessories,
            'new_items':new_item,
        }
        return render(request,'index.html',context)


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            # messages.add_message(request,messages.ERROR,'Вы уже зарегистрированы')
            return redirect('home')
        form=RegistrationForm(request.POST or None)
        title = 'Регистрация'
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'registration.html',context)
    
    def post(self,request,*args,**kwargs):
        form= RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            new_user.first_name=form.cleaned_data['first_name']
            new_user.last_name=form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            # oldname = request.session.session_key
            # oldorders = Order.objects.filter(customer__user__username=oldname)
            # customer = Customer.objects.create(
            #     user=new_user,
            #     phone=form.cleaned_data['phone'],
            # )
            # customer.save()

            # if oldorders:
            #     customer.orders.set(oldorders)
            #     for i in oldorders:
            #         i.customer = customer
            #         i.customer.save()
            #         i.save()
                
                # User.objects.filter(username=oldname).delete()
                
            user= authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            # messages.add_message(request,messages.SUCCESS,'Вы успешно зарегистрировались на сайте')
            return redirect('home')
        # else:
        #     messages.add_message(request,messages.ERROR,'Ошибка регистрации')
        context={'form':form,}
        return render(request,'registration.html',context)


class LoginView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            # messages.add_message(request,messages.ERROR,'Вы уже залогинены')
            return redirect('home')
        form = LoginForm(request.POST or None)
        # category = Category.objects.all()
        title = 'Логин'
        context= {'title':title,
        'form':form,
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                user1= User.objects.filter(email=username).first()
                user= authenticate(username=user1,password=password)
            else:
                user= authenticate(username=username,password=password)
            if user:
                login(request,user)
            return HttpResponseRedirect('/')
        context={'form':form,}
        return render(request,'login.html',context)


class ProductDetailView(DetailView):
    context_object_name='product'
    model= Product
    template_name='product_detail.html'
    slug_url_kwarg='slug'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        s=ProductFeatures.objects.filter(product=self.get_object()).first()
        items = Product.objects.filter(Q(features=s)|Q(title=self.get_object().title)).distinct()[:4]
        # похожие товары
        # query = self.request.GET.get('search')
        # context['categories'] =  self.get_object().category.__class__.objects.all()
        # context['cart']= self.cart
        context['items']=items
        context['title'] = self.get_object().title
        category=self.get_object().category
        # context['randomProducts']= Product.objects.filter(category=category)[:12]
        return context



class CategorytDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        category = self.get_object()
        context['categories'] = self.model.objects.all()
        context['title']=self.get_object().name
        context['tags']= Tag.objects.all()
        if not query and not self.request.GET:
            context['category_products'] = category.product_set.all()
            return context
        if query:
            products = category.product_set.filter(Q(title__icontains=query))
            context['category_products'] = products
            return context
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        q_condition_queries = Q()
        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
            else:
                q_condition_queries.add(Q(**{'value': value}), Q.OR)
        pf = ProductFeatures.objects.filter(
            q_condition_queries
        ).prefetch_related('product', 'feature').values('product_id')
        products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
        context['category_products'] = products
        return context


class AddtoWhishlistView(View):
    def get(self,request,*args,**kwargs):
        product_slug= kwargs.get('slug')
        product= Product.objects.get(slug=product_slug)

        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user).first()
            # Whishlist.objects.get_or_create(owner=user,products=product)
            try:
                whish=Whishlist.objects.get(owner=user,products=product)
            except Exception as e:
                new_whish = Whishlist(owner=user,products=product,whishlist=True)
                new_whish.save()
        else:
            name = str(request.session.session_key)
            # Whishlist.objects.get_or_create(session=name,products=product)
            try:
                whish=Whishlist.objects.get(session=name,products=product)
                if whish:
                    whish.delete()
            except Exception as e:
                new_whish = Whishlist(session=name,products=product,whishlist=True)
                new_whish.save()

        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))

    

class WhislistView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            name = request.user
            user = User.objects.filter(username=name).first()
            favorite = Whishlist.objects.filter(owner=user)
        else:
            name = str(request.session.session_key)
            favorite = Whishlist.objects.filter(session=name)

        title='Избранное'
        return render(request,'whishlist.html',{'title':title,
                'favorite':favorite })



class DeleteFromWhislist(View):

    def get(self,request,*args,**kwargs):

        product_slug=kwargs.get('slug')
        product= Product.objects.get(slug=product_slug)

        if request.user.is_authenticated:
            name = request.user
            user = User.objects.filter(username=name).first()
            Whishlist.objects.get(owner=user,products=product).delete()
        else:
            name = str(request.session.session_key)
            Whishlist.objects.get(session=name,products=product).delete()

        # messages.add_message(request,messages.INFO,'Товар удален из избранного')
        return HttpResponseRedirect('/whishlist/')


class SearchProduct(ListView):
    template_name = 'product-search.html'
    context_object_name = 'products'
    # paginate_by = 9
    def get_queryset(self):
        search= self.request.GET.get('search')
        print(search)
        if search:
            if search[0].lower():
                search=search.title()
        return Product.objects.filter(Q(title__icontains=search))
    
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Поиск по сайту: '+str(self.request.GET.get('search'))
        # context['category']=Category.objects.order_by('?').first()
        context['s']=f"s={self.request.GET.get('search')}&"
        return context


# class AllProducts(ListView):

#     template_name = 'products.html'
#     context_object_name = 'products'
#     # paginate_by = 9

#     return Product.objects.all()
    
#     def get_context_data(self,*,object_list=None,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title']='Все товары'
#         return context



class AllProducts(ListView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'products.html'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Все товары'
        
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        if url_kwargs:
            q_condition_queries = Q()
            for key, value in url_kwargs.items():
                if isinstance(value, list):
                    q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
                else:
                    q_condition_queries.add(Q(**{'value': value}), Q.OR)
            pf = ProductFeatures.objects.filter(
                q_condition_queries
            ).prefetch_related('product', 'feature').values('product_id')
            products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
            context['products'] = products
        return context
