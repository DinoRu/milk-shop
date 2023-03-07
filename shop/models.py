from django.db import models


CATEGORIE_CHOICES = (
    ('ML', 'Milk'),
    ('MS', 'MilkShake'),
    ('CR', 'Curd'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-Creams'),
    ('LS', 'Lassi'),
)

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discount_price = models.FloatField(blank=True)
    discription = models.TextField(default="")
    compositions = models.TextField(default="")
    prodapp = models.TextField(default="")
    category = models.CharField(choices=CATEGORIE_CHOICES, max_length=2)
    prod_image = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.title
