from django.contrib import admin

# Register your models here.
class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):

        extra_context = extra_context or {}
        extra_context['failed_transactions'] = "1"

        return super().index(request, extra_context=extra_context)
    
admin_site = MyAdminSite(name="admin")