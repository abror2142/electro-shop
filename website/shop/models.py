from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from accounts.models import Customer


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Davlat'
        verbose_name_plural = 'Davlatlar'


class Brand(models.Model):
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Brend'
        verbose_name_plural = 'Brendlar'


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    views = models.IntegerField(default=0)
    produced_at = models.DateField(default=now)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default='')
    details = models.TextField(default='')
    discount = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, default=None, on_delete=models.DO_NOTHING, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def get_discount_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount) / 100
        else:
            return 0

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Mahsulot Rasm'
        verbose_name_plural = 'Mahsulot Rasmlari'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name = 'Komment'
        verbose_name_plural = 'Kommentlar'

# Order Products


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} {self.created}"

    @property
    def get_cart_total_price(self):
        products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in products])
        return total_price

    @property
    def get_total_cart_product(self):
        return len(self.orderproduct_set.all())

    @property
    def get_cart_product_number(self):
        products = self.orderproduct_set.all()
        total_number = sum([product.quantity for product in products]) or 0
        return total_number

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.order} {self.product}"

    @property
    def get_total_price(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = 'Buyurtma va Mahsulot'
        verbose_name_plural = 'Buyurtmalar va Mahsulotlar'


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Shipping(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100)
    district = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    zip_code = models.IntegerField()
    mobile = models.CharField(max_length=13)
    email = models.EmailField()

    def __str__(self):
        return f"{self.order} {self.city}"

