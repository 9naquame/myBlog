from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Blog, Comment
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.decorators import login_required

class SearchForm(forms.Form):
        search = forms.CharField(label='Enter Search Term')


class CommentForm(ModelForm):
        class Meta:
                model = Comment
                exclude = ['post','author']
        
def home(request):
        blog_list = Blog.objects.all()[:3]
        if not request.user.is_authenticated():
                return render_to_response('base.html', {'blog_list':blog_list,'request_user':request.user.username})
        return render_to_response('base.html', {'blog_list':blog_list,'request_user':request.user.username,'full_name':request.user.get_full_name()})

        
@csrf_exempt
def blog_detail(request, id, showComments=False):
        blog = Blog.objects.get(pk=id)
        comments = Comment.objects.filter(post__pk=id)
        #Start of form code
        if request.method == 'POST':
            comment = Comment(post=blog,author=request.user.username)
            form = CommentForm(request.POST,instance=comment)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.path)
        else:
                form = CommentForm()
        #end of form code               
        return render_to_response('blog/detail.html',{'blog':blog, 'comments':comments,'form':form.as_p(),'request_user':request.user.username})

        
@csrf_exempt
def searchView(request):
        blog_list = Blog.objects.all()[:3]
        if request.method == 'POST':
                form = SearchForm(request.POST)
                if form.is_valid():
                        term = form.cleaned_data['search']       
                        getSearch = Blog.objects.filter(title__icontains=term)
                        return render_to_response('blog/search.html', {'blog_list':blog_list,'getSearch':getSearch,'term':term})
        else:   
                form = SearchForm()
        return render_to_response('blog/searchpage.html', {'form': form,'blog_list':blog_list})
        
        
        
def blog_search(request, term):
        getSearch = Blog.objects.filter(title__icontains=term)
        blog_list = Blog.objects.all()[:3]
        return render_to_response('blog/search.html',{'blog_list':blog_list,'getSearch':getSearch,'term':term})
        
        
@csrf_exempt
def editcomment(request, id):
        comment = Comment.objects.get(pk=id) #Comment.objects.filter(pk=id)[0]
        t = loader.get_template('blog/editcomment.html')
        if request.method == 'POST':
            form = CommentForm(request.POST,instance=comment)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/blog/detail/'+str(comment.post.id)+'/True')
        else:
                if request.user.is_authenticated():
                        form = CommentForm(instance=comment)
                        c = Context({'comment':comment,'form':form.as_p(),'request_user':request.user.username})
                        return HttpResponse(t.render(c))
