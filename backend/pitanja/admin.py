from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from pitanja.models import *


class UcenikInline(admin.StackedInline):
    model = Ucenik
    can_delete = False
    verbose_name_plural = 'učenici'


class UserAdmin(BaseUserAdmin):
    inlines = (UcenikInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Skola)
admin.site.register(Ucenik)
admin.site.register(Test)
admin.site.register(Pitanje)
admin.site.register(Odgovor)
admin.site.register(TestUcenika)
admin.site.register(OdgovorUcenika)
