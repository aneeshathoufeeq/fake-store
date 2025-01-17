from django.db import models
from django.contrib.auth.models import User

# pillow:helps support graphical content in django

# Create your models here.
class Categorymodel(models.Model):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='imagess',null=True)
    def __str__(self):
        return self.category_name

class Productmodel(models.Model):
    product_name=models.CharField(max_length=100)
    product_image=models.ImageField(upload_to='imagess',null=True)
    product_description=models.TextField(null=True)
    product_price=models.IntegerField()
    product_stock=models.IntegerField()
    product_category=models.ForeignKey(Categorymodel,on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name
    


class CartModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True )
    product=models.ForeignKey(Productmodel,on_delete=models.CASCADE,null=True)
    total_price=models.DecimalField(decimal_places=2,max_digits=10,null=True)
    Date=models.DateTimeField(auto_now_add=True)



class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True )
    product=models.ForeignKey(Productmodel,on_delete=models.CASCADE,null=True)
    orderdate=models.DateTimeField(auto_now_add=True)
    Addreess=models.CharField(max_length=1000)

    

