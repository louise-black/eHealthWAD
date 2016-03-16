from django.contrib import admin

from healthApp.models import Category, Page

from healthApp.models import UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}



admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
