from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    category        = models.ForeignKey(Category , on_delete=models.CASCADE)
    product_name    = models.CharField(max_length=250,unique=True)
    slug            = models.SlugField(max_length=550,unique=True)
    discription     = models.TextField()
    price           = models.IntegerField()
    stock           = models.IntegerField()
    product_image   = models.ImageField(upload_to='media/product/', blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    modefied        = models.DateTimeField(auto_now=True)
    is_avalible     = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug,])
    

variation_catagiry_choices=(
    ('color','color'),
    ('size','size'),
)

class variationmanager(models.Manager):
    def color(self):
        return super(variationmanager,self).filter(variation_category='color',is_active=True)
    def size(self):
        return super(variationmanager,self).filter(variation_category='size',is_active=True)
    
class variations(models.Model):
    product               = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category    = models.CharField(max_length=50, choices=variation_catagiry_choices)
    variation_value       = models.CharField(max_length=50)
    is_active             = models.BooleanField(default=True)
    created               = models.DateField(auto_now_add=True)

    objects=variationmanager()

    def __str__(self):
        return self.variation_value






