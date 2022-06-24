from django.forms import ModelForm
from product.models import Category, Product


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ("category", "name", "image_1", "image_2", "image_3", "image_4", "description", "price", "stock")
        
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            

class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("category_name", "category_image", "category_description")
        
    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"