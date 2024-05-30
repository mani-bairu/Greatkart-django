from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    caterogy_name   = models.CharField(max_length=250,unique=True)
    slug            = models.SlugField(max_length=500,unique=True)
    discription     = models.TextField()
    cat_image       = models.ImageField(upload_to= "media/category/" ,blank=True )

    def __str__(self):
        return self.caterogy_name
    
    def get_url(self):
        return reverse('get_product_by_category',args=[self.slug])

