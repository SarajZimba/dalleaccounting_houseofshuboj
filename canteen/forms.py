from django import forms
from django.forms.models import inlineformset_factory
from root.forms import BaseForm  # optional

from .models import StudentAttendance

class StudentAttendanceForm(BaseForm, forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)