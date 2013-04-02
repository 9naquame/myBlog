from django.db import models
from django.contrib import admin
from CountryField import CountryField

class Blog(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    country = CountryField(default='',max_length=3)
    def __unicode__(self):
        return self.title


class Comment(models.Model):
	author = models.CharField(max_length=60)
	body = models.TextField()
	created = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	post = models.ForeignKey(Blog)
	
	def body_(self):
            return self.body[:160]
        
	def __unicode__(self):
		return self.body
	    

class CommentInline(admin.StackedInline):
	model = Comment
	extra = 1
	

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title','created','updated')
	search_fields = ('title','body')
	list_filter = ('created',)
	inlines = [CommentInline]
	def __unicode__(self):
		return self.list_display
	

class CommentAdmin(admin.ModelAdmin):
	list_display = ('post','author','body_','created','updated')
	search_fields = ('author','body')
	list_filter = ('created','author')
	def __unicode__(self):
		return self.list_display



admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment,CommentAdmin)
	
