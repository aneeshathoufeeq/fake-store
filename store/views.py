from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,ListView,DetailView,UpdateView
from store.models import User,Categorymodel,Productmodel,CartModel,Order
from store.forms import User_reg_form,Loginform,Category_form,Product_form,orderform
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwrgs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwrgs)
    return wrapper

def mylogin(fn):
    def wrapper(request,*args,**kwrgs):
        
        id=kwrgs.get("pk")
        data=CartModel.objects.get(id=id)
        if data.user!=request.user:
            return redirect("signin")
        else:
            return fn(request,*args,**kwrgs)
    return wrapper


class Userlogout(View):
    def get(self,request,*args,**kwrgs):
        logout(request)
        return redirect('signin')



class User_register(View):

    def get(self,request,*args,**kwargs):
        form=User_reg_form() 
        return render(request,"register.html",{"form":form})


    def post(self,request,*args,**kwargs):

        form=User_reg_form(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            f_name=form.cleaned_data.get('first_name')
            l_name=form.cleaned_data.get('last_name')
            user=User.objects.create_user(username=u_name,first_name=f_name,last_name=l_name,email=email,password=password)

               
            subject='Welcome to fakestore'
            message=f'hi {user.username}thank you for registering fakesore'
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[user.email,]
            send_mail(subject,message,email_from,recipient_list ) 
            print(message)
        form=User_reg_form()
        return render(request,"login.html",{"form":form })
    

# UserRegister


       
class Userlogin(View):

    def get(self,request,*args,**kwrgs):

        form=Loginform()
        return render(request,"login.html",{"form":form})



    def post(self,request,*args,**kwrgs):

        form=Loginform(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')

            usr_obj=authenticate(username=u_name,password=pwd)
            
            if usr_obj:
                print("Valid credentials")
                login(request,usr_obj)
            # form=Loginform()
        return render(request,"category.html")
            
       

# Vender registeration
# python manage.py createsuperuser
# Username: admin
# Email address: aneeshamol555@gmail.com
# Password:
# Password (again):


class Vregisteration(View):
    def get(self,request,*args,**kwrgs):
        form=User_reg_form()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwrgs):
        form=User_reg_form(request.POST)
        if form.is_valid():
            User.objects.create_superuser(**form.cleaned_data)
        form=User_reg_form()
        return redirect(request,"login.html",{"form":form})
    
# lh:8000/store/add/
class Addcategory(CreateView):
    model=Categorymodel
    form_class=Category_form
    template_name="category.html"
    success_url=reverse_lazy('register')

 

# class Addproduct(CreateView):
#     model=Productmodel
#     form_class=Product_form
#     template_name="product.html"
#     sucess_url=reverse_lazy('register')

# from django.urls import reverse_lazy

class Addproduct(CreateView):
    model = Productmodel
    form_class = Product_form
    template_name = "product.html"
    success_url = reverse_lazy('register')  



class Category_list(ListView):
    model=Categorymodel
    template_name="category.html"
    context_object_name="categories"




    

class Product_list(ListView):
    model=Productmodel
    template_name="product.html"
    context_object_name="product"





# class ProductDetail(View):
#     def get(self, request, pk):
#         product = get_object_or_404(Productmodel, pk=pk)  # Retrieve product by primary key
#         return render(request, "product_detail.html", {"product": product})


 

class ProductDetail(View):
    def get(self,request,*args,**kwrgs):
       id=kwrgs.get("pk")
       print("id",id)
       print("hiii")
       data=Productmodel.objects.get(id=id)
       print(data)
       return render(request,"product_detail.html",{"product_detail":data})


    
    


@method_decorator(mylogin,'dispatch')
@method_decorator(signin_required,name='dispatch')

class ProductUpdate(UpdateView):
    
    model=Productmodel

    success_url=reverse_lazy("vproduct")




class CategoryDetail(View):
    def get(self,request,*args,**kwrgs):
        id=kwrgs.get("pk")
        print("id",id)
        data=Productmodel.objects.filter(product_category_id=id)
        print(data)
        return render(request,"product.html",{"product":data})



@method_decorator(signin_required,name='dispatch')

class AddToCartView(View):
    def get(self,request,**kwrgs): 

        id=kwrgs.get("pk")

        data=Productmodel.objects.get(id=id)
        # getting product object from from product_model using the id
        
        CartModel.objects.create(user=request.user,product=data)
# adding the product  object to the cartmodel
    
        c_data=CartModel.objects.filter(user=request.user)
    #    filtering th e objects from the cart_model
        print(c_data)
        total_price=0
        for i in c_data:
            # more than one objects in cart_madel so using for loop for iterating.


            if i.product and hasattr(i.product,'product_price'):
                #  checking if the object has the field product and does it have the connecting fileld product_price
            
                 total_price+=i.product.product_price
                 print("price",total_price)

        return render(request,"card.html",{"c_data":c_data,"total_price":total_price})




# @method_decorator(mylogin,'dispatch')
# @method_decorator(signin_required,name='dispatch')
class CartDelete(View)  :
    def get(self,request,**kwrgs):

        id=kwrgs.get("pk")

        cart_items = CartModel.objects.filter(product_id=id)
        for i in cart_items:
            i.delete()
            print("deleted sucessfully")

        return redirect('viewcart')
    


class CategoryDetail(View):
    def get(self,request,*args,**kwrgs):
        id=kwrgs.get("pk")
        print("id",id)
        data=Productmodel.objects.filter(product_category_id=id)
        print(data)
        return render(request,"product.html",{"product":data})


class CartView(View):

    def get(self,request,**kwrgs): 
        cartdata=CartModel.objects.filter(user=request.user)
    #    filtering th e objects from the cart_model
        print(cartdata)
        total_price=0
        for i in cartdata:

            if i.product and hasattr(i.product,'product_price'):
                #  checking if the object has the field product and does it have the connecting fileld product_price
            
                 total_price+=i.product.product_price
                 print("price",total_price)

        return render(request,"card.html",{"c_data":cartdata,"total_price":total_price})
    
class OrderView(View):
    def get(self,request,**kwrgs):
        id=kwrgs.get("pk")
        data=CartModel.objects.get(id=id)
    
        form=orderform()
        return render(request,"order.html",{"data":data,"form":form})
    
    def post(self,request,**kwrgs):
        id=kwrgs.get("pk")
  
        data=CartModel.objects.get(id=id)
        form=orderform(request.POST)
        if form.is_valid():
            Order.objects.create(user=request.user,product=data,**form.cleaned_data)
        CartModel.objects.filter(user=request.user)(product_id=id).delete()
        return render(request,"order.html",{"data":data,"form":form})
    



# @method_decorator(mylogin,'dispatch')
@method_decorator(signin_required,name='dispatch')

class OrderList(View):
    def get(self,request,*args,**kwargs):
        data=Order.objects.filter(user=request.user)
        return render(request,"orderlist.html",{"data":data})
    
