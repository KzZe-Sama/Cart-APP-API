from django.db import models
import uuid

from django.db.models.fields import UUIDField

from accounts.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return  self.name 
def upload_to(instance,filename):
    return f'images/{filename}'.format(filename)
class Item(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255,blank=True)
    title = models.CharField(max_length=25,blank=False)
    description = models.TextField(default="")
    quantity = models.IntegerField()
    price = models.IntegerField(blank=False)
    image = models.ImageField(upload_to=upload_to,default="/images/default.png") 
    # print(category)
    def save(self, *args, **kwargs):
        self.category_name = self.category.name
        # print(self.title)
        super(Item, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.category} {self.title}' 

class Review(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.TextField(max_length=255)
    def __str__(self):
        return f'{self.user} {self.item}'

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.product}'

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20);    
    total_items = models.IntegerField(default=0)
    address = models.TextField();
    delivery_date = models.DateField(blank=True);
    payment_option = models.CharField(max_length=50);
    total_amount = models.IntegerField()
    is_delivered = models.BooleanField(default=False,auto_created=True)
    is_refunded = models.BooleanField(default=False,auto_created=True)
    is_canceled = models.BooleanField(default=False,auto_created=True)
    delivery_charge = models.IntegerField(default=100)
    def __str__(self):
        return str(self.uuid)

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    price = models.IntegerField();
    
    def __str__(self):
        return str(f'Order_ID:#{str(self.order_id.uuid)} {str(self.item_id.title)}')

class Like(models.Model):
    product_id = models.ForeignKey(Item,on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_id} liked by {self.liked_by}'