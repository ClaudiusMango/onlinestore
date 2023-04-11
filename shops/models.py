from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe

class Shop(models.Model):
    shop_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    instagram_link = models.CharField(max_length=1000, null=True, blank=True)
    facebook_link = models.CharField(max_length=1000, null=True, blank=True)
    twitter_link = models.CharField(max_length=1000, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=12, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    location = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        try:
            return self.shop_name
        except:
            return super().__str__()
        
    @property
    def product_category_list(self):
        return self.product_categories.all()
    
class ProductCategory(models.Model):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name='product_categories')
    category_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.category_name
    
    class Meta:
        ordering = ["category_name"]

    @property
    def stripped_name(self):
        str = self.category_name.lower()
        new_str = str.replace(" ", "-")
        return new_str

    @property
    def sub_category_list (self):
        return self.sub_categories.all()
    
    @property
    def products(self):
        products = []
        for sub_category in self.sub_categories.all():
            products += sub_category.products.all()

        return products

class ProductSubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory,on_delete = models.CASCADE, related_name='sub_categories')

    def __str__(self) -> str:
        try:
            return self.subcategory_name
        except:
            return super().__str__()
        
    class Meta:
        ordering = ["subcategory_name"]

class Product(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE, related_name="products")
    product_category = models.ForeignKey(ProductSubCategory,on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField()
    product_image = models.ImageField(null=True,upload_to="productimages")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product_name

    class Meta:
        ordering = ["-date_added"]

    @property
    def image_url(self):
        try:
            url = self.product_image.url
        except:
            url = ''

        return url

    @property
    def product_features(self):
        return self.productfeature_set.all()

    @property
    def product_images(self):
        return self.productimage_set.all()

    @property
    def product_relative_url(self):
        return reverse('product_details', kwargs={'product_id':self.id})
    
class ProductFeature(models.Model):
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=255)
    feature_description = models.TextField()

    def __str__(self) -> str:
        return self.feature_name

class ProductImage(models.Model):
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    image= models.ImageField(upload_to="productimages")

    def __str__(self) -> str:
        return self.image.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url
    
class Order(models.Model):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(f'{self.customer_name} Date:{self.date_ordered.date()}')
    
    class Meta:
        ordering = ["-date_ordered"]
    
    @property
    def customer_name(self):
        return f"{self.checkoutinfo.first_name} {self.checkoutinfo.last_name}"
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    @property
    def cart_items(self):
        return self.orderitem_set.all() 

    def order_details(self):
        orderitems = self.orderitem_set.all()
        table_items = ""
        for item in orderitems:
            table_item = f'<tr><td>{item.product.product_name}</td><td>{item.quantity}</td><td>{item.get_total} Ksh</td></tr>'
            table_items+=table_item
            return mark_safe(
                f'''
                    <p>Date: {self.date_ordered.date()} {self.date_ordered.time()}</p>
                    <p>Name: {self.checkoutinfo.first_name} {self.checkoutinfo.last_name}</p>
                    <p>Phone number: {self.checkoutinfo.phone_number}</p>
                    <p>Delivery Option: {self.checkoutinfo.delivery_option}</p>
                    <p>Items Ordered:</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Product name</th>
                                <th>Quantity</th>
                                <th>Item total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_items}
                            <tr>
                                <td colspan= "2" >Order total</td>
                                <td>{self.get_cart_total} Ksh</td>
                            </tr>
                        </tbody>
                    </table>
                '''
            )
        
        # return html

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class CheckOutInfo(models.Model):
    PICKUP_CHOICES=[
        ('pickup','Store pick-up'),
        ('home_delivery','Home Delivery'),
        ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    delivery_option = models.CharField(choices=PICKUP_CHOICES,max_length=200)
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, null = True)