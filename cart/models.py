from django.db import models
from store.models import Product,variations
from accounts.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id       = models.CharField(max_length=500,)
    date_added    = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class Cart_items(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    product    = models.ForeignKey(Product , on_delete=models.CASCADE)
    variation  = models.ManyToManyField(variations , blank=True,null=True)
    cart       = models.ForeignKey(Cart , on_delete=models.CASCADE,null=True)
    quantity   = models.IntegerField()
    is_active  = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product.product_name
