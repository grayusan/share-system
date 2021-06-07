from django.contrib import admin
from .models import Post #Comment, Reply

'''
class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5


class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
'''

class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text', 'allowed_list')
    list_display = ['title', 'created_at', 'title_len', 'allowed_list']
    ordering = ('-created_at',)

    def title_len(self, obj):
        return len(obj.title)

    title_len.short_description = 'words count title'

admin.site.register(Post, PostAdmin)