from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile, Comment

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('category','username','timesmp','content')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment,CommentAdmin)

