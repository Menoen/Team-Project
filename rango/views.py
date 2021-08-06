from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category,Page,Comment
from rango.forms  import CategoryForm, CommentForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.conf import settings
from pathlib import Path
from django.views import View


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['extra'] = 'From the model solution on GitHub'

    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # Spoiler: now you DO need a context dictionary!
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        comment = Comment.objects.filter(category=category).order_by('-timesmp')
        context_dict['pages'] = pages
        context_dict['category'] = category
        # comment form
        form = CommentForm()
        context_dict['form'] = form
        for c in comment:
            print(c.username)
            path = Path(settings.MEDIA_ROOT+'/profile_images/'+c.username+'.jpg')
            c.pic_exist = path.exists()
        context_dict['comments'] = comment

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
        context_dict['comments'] = None
        context_dict['form'] = None
        context_dict['pic_exist'] = None

    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query

    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
        
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'rango/register.html', context = {'user_form': user_form,
                                                             'profile_form': profile_form,
                                                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def add_comment(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print('valid')
            if category:
                comment = form.save(commit=False)
                comment.category = category
                print(request)
                if request.user.is_authenticated:
                    comment.username = request.user.username
                else:
                    comment.username = "Anonymous"
                comment.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print('not valid')
            print(form.errors)
    
    show_category(request,category_name_slug)
def get_category_list(max_results=0, starts_with=''):
    category_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]
    return category_list


class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        category_list = get_category_list(max_results=8, starts_with=suggestion)

        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')

        return render(request, 'rango/categories.html', {'categories': category_list})


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
    try:
        page = Page.objects.get(id=page_id)
        page.views = page.views + 1
        page.save()
        url = page.url
    except:
        pass
    return redirect(url)

@login_required
def like_category(request):
    categoryName = None
    if request.method == 'GET':
        categoryName = request.GET['category_name']
        likes = 0
        if categoryName:
            category = Category.objects.get(id = int(categoryName))
            if category:
                likes = category.likes +1
                category.likes = likes
                category.save()
    return HttpResponse(likes)