from django.contrib import admin
from .models import Post, Category, Comments, Slider, Widgets, SocialShare, Theme
from django.conf import settings
from bs4 import BeautifulSoup
from django.utils.translation import ugettext_lazy as _


class MyAdminSite(admin.AdminSite):
    site_header = settings.SITE_TITLE + ' administration'


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fieldsets = [
        ('none', {'fields': ['name', 'menu_type', 'menu_order']})
    ]
    list_display = ('name', 'slug', 'menu_type')


class PostAdmin(admin.ModelAdmin):
    model = Post
    fieldsets = [
        ('none', {'fields':['title', 'category', 'content']}),
        ('none', {'fields':['type', 'comment_status', 'menu_order', 'status']}),
    ]
    inlines = []
    list_display = ('title', 'author', 'status', 'category', 'created_date', 'url_link', 'type', 'views_count', 'menu_order')
    list_filter = ['created_date', 'category', 'type', 'status']
    search_fields = ['title', 'content']

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'author'):
            obj.author = request.user
        content = BeautifulSoup(obj.content)
        img_link = content.find_all('img')[0].get('src')
        obj.image = img_link
        obj.save()


class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ('author', 'content', 'status', 'created_date', 'post')
    list_filter = ['status']
    search_fields = ['content', 'author']


class SliderAdmin(admin.ModelAdmin):
    model = Slider
    fieldsets = [
        ('Slider', {'fields':['title', 'image_file', 'location']}),
        ('Opciones', {'fields': ['link_target', 'content', 'order', 'status', 'until_date']})
    ]
    list_display = ('title', 'link_target', 'image_file', 'until_date', 'location', 'is_active', 'order')
    list_filter = ('status', 'created_date', 'location')
    search_fields = ('title', 'content', 'link_target')


class WidgetsAdmin(admin.ModelAdmin):
    model = Widgets
    fieldsets = [
        ('Slider', {'fields':['title', 'image_file', 'content']}),
        ('options', {'fields': ['link_target', 'order', 'status', 'until_date']})
    ]
    list_display = ('title', 'link_target', 'image_file', 'until_date', 'created_date', 'is_active', 'order')
    list_filter = ('status', 'created_date')
    search_fields = ('title', 'content', 'link_target')


class SocialShareAdmin(admin.ModelAdmin):
    model = SocialShare
    fieldsets = [
        ('none', {'fields':['name', 'html_code', 'js_code']}),
        ('options', {'fields': ['status', 'order']})
    ]

class ThemeAdmin(admin.ModelAdmin):
    model = Theme
    list_display = ('name', 'status', 'created_date', 'file_name')
    list_filter = ('created_date', 'status')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Widgets, WidgetsAdmin)
admin.site.register(SocialShare, SocialShareAdmin)
admin.site.register(Theme, ThemeAdmin)