from django import forms
from .models import Order, Payment

class OrderForm(forms.ModelForm) :
    class Meta :
        model = Order
        fields = ['full_name', 'mobile', 'address', 'city', 'pin_code', 'state', 'country', 'landmark', 'message']
        
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        

class PaymentForm(forms.ModelForm) :
    class Meta :
        model = Payment
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"