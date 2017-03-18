from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor
from models import Good, Bid, Image

# Register your models here.
admin.site.register(Good)
admin.site.register(Bid)
admin.site.register(Image)


class GoodAdminForm(forms.ModelForm):
    class Meta:
        model = Good
        widgets = {
            'short_text': RedactorEditor(),
        }
        #  fields = '__all__'
        fields = ('details',)


class GoodAdmin(admin.ModelAdmin):
    form = GoodAdminForm
