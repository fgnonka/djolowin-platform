# bundle/admin.py
from django.contrib import admin
from .models import Bundle, PlayerCard
from .forms import BundleForm

class PlayerCardInline(admin.TabularInline):
    model = Bundle.cards.through

class BundleAdmin(admin.ModelAdmin):
    form = BundleForm
    inlines = [PlayerCardInline,]
    exclude = ('cards',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "cards":
            if request._obj_ is not None:
                kwargs["queryset"] = PlayerCard.objects.filter(cardbundle=request._obj_)
            else:
                kwargs["queryset"] = PlayerCard.objects.none()
        return super(BundleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(BundleAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Bundle, BundleAdmin)
