from django import forms
from django.forms.models import inlineformset_factory
from root.forms import BaseForm  # optional

from .models import ProductCategory
from accounting.models import AccountLedger

class ProductCategoryForm(BaseForm, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]


from .models import Product


class ProductForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "image",
            "description",
            "product_id",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["price"].label = "Selling Price"
        self.fields['ledger'] = forms.ModelChoiceField(queryset=AccountLedger.objects.all().order_by('ledger_name'), required=False)
        self.fields["ledger"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }
    def clean(self):
        cleaned_data = super().clean()
        is_canteen_item = cleaned_data.get("is_canteen_item")
        lunch_type = cleaned_data.get("lunch_type")

        if is_canteen_item and not lunch_type:
            self.add_error("lunch_type", "Lunch type is required for canteen items.")

        # Optional: clear lunch_type if not a canteen item
        if not is_canteen_item:
            cleaned_data["lunch_type"] = None

        return cleaned_data

from .models import CustomerProduct


class CustomerProductForm(BaseForm, forms.ModelForm):
    class Meta:
        model = CustomerProduct
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "agent",
        ]

from .models import ProductStock

class ProductStockForm(BaseForm, forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]

from .models import BranchStock
class BranchStockForm(BaseForm, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False))
        self.fields["product"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }

    class Meta:
        model = BranchStock
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at','sorting_order', 'is_featured']
        
from organization.models import Branch
from .models import RequisitionBranchStock
class RequisitionBranchStockForm(BaseForm, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False))
        self.fields["product"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }
        self.fields['branch'] = forms.ModelChoiceField(queryset=Branch.objects.filter(is_deleted=False))
        self.fields["branch"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Branch",
        }

    class Meta:
        model = RequisitionBranchStock
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at','sorting_order', 'is_featured']