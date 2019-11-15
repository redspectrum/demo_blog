from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from .models import Post, Tag, Collection, Picture
from django.views import View
from .forms import CreatePostForm, CreateCollectionForm, FileFieldForm

def welcome(request):
    name = 'Vasia'
    return render(request, template_name='blog/welcome.html',context={'name': name})


def posts(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()
    collections = Collection.objects.all()
    return render(request, template_name='blog/posts.html',context={'posts': posts,
                                                                    'tags': tags,
                                                                    'collections': collections})

def post(request, slug=None):
    if slug:
        post = get_object_or_404(Post, slug=slug)
        return render(request, template_name='blog/post.html',context={'post': post})
    raise Http404("No MyModel matches the given query.")


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = FileFieldForm()
    return render(request, 'upload.html', {'form': form})



def collection(request, slug=None):
    collection = get_object_or_404(Collection, slug=slug)

    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                create_pic = Picture.objects.create(url=f)
                # a.save()
                collection.pictures.add(create_pic)
                collection.save()
            # Add message - Successfully upload!
        else:
            raise Http404("Bad files")
    if slug:
        form = FileFieldForm()
        pics = Picture.objects.all()
        return render(request, template_name='blog/collection.html',context={'collection': collection, 'form': form, 'pics': pics})
    raise Http404("No MyModel matches the given query.")

def delete_picture(request, url=None):
    obj = Picture.objects.get(url__iexact=url)
    obj.delete()
    return redirect('posts')

# def post_create(request):
#
#     form = CityViewForm()
#     context = {
#         'name': 'index',
#         'form': form
#     }
#     return render(request, template_name='blog/create_post.html', context=context)




def post_create(request):

    form = CreatePostForm()
    context = {
        'name': 'index',
        'form': form
    }

    return render(request, template_name='blog/create_post.html', context=context)


def create_collection(request):
    form = CreateCollectionForm()
    context = {
        'name': 'index',
        'form': form
    }
    return render(request, template_name='blog/create_collection.html', context=context)



# class PostCreate(View):
#     model_form = CreatePostForm
#     template = 'blog/create_post.html'
#     raise_exception = True
#
#     def get(self, request):
#         form = self.model_form()
#         return render(request, self.template, context={'form': form})
#
#     def post(self, request):
#         bound_form = self.model_form(request.POST)
#
#         if bound_form.is_valid():
#             new_obj = bound_form.save()
#             return redirect(new_obj)
#         return render(request, self.template, context={'form': bound_form})


# ==========================================
from django.conf import settings
import os
import glob
import uuid

def image_form(request):

    template_name = 'blog/image-form.html'
    username = request.user.get_username()
    mypath = settings.MEDIA_ROOT + '/' + username

    all_url_pics = glob.glob(mypath+ '/*.jpg')
    pics = [pic.replace(settings.BASE_DIR, '..') for pic in all_url_pics]
    return render(request, template_name, context={'pics':pics})




def add_unique_name(mypath, image_name):
    all_url_pics = glob.glob(mypath +'/*.jpg')
    image_url = mypath + '/' + image_name
    print('all_url_pics=',all_url_pics)
    print('image_url=',image_url)

    if image_url in all_url_pics:
        image_name = '{}_{}.jpg'.format(image_name[:-4], uuid.uuid4())
    return image_name


def image_upload(request):
    username = request.user.get_username()

    mypath = settings.MEDIA_ROOT + '/' + username
    if not os.path.isdir(mypath):
        os.makedirs(mypath)

    for count, x in enumerate(request.FILES.getlist('files')):
        def process(f):
            print('XXXXXXXX:', f.name)
            f.name = add_unique_name(mypath, f.name)
            print('XXXXXXXX:', f.name)
            with open(mypath +'/'+f.name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)

    return redirect('image_form')


# ==========================================