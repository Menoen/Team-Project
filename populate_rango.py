import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, Comment
from django.utils import timezone

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 1},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': 2},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorial/python/',
         'views': 4}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'http://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': 8},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/',
         'views': 16},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': 32}
    ]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/',
         'views': 64},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org/',
         'views': 128}
    ]
    
    python_comment = [
        {
         'username': 'zhao_weiwei',
         'timesmp': timezone.now(),
         'content':'123421dsdasdasdd'
        },
        {
         'username': 'zhao_weiwei',
         'timesmp': timezone.now(),
         'content':'sdfsfasfadsfasd'
        }
    ]
    django_comment = [
        {
         'username': 'an',
         'timesmp': timezone.now(),
         'content':'123421dsdasdasdd'
        },
        {
         'username': 'dddd',
         'timesmp': timezone.now(),
         'content':'sdsdsdsd'
        }
    ]
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64, 'comments': python_comment},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32, 'comments': django_comment},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16, 'comments': []}
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
        for m in cat_data['comments']:
            add_comment(c, m['username'], m['timesmp'], m['content'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
        for m in Comment.objects.filter(category=c):
            print(f'- {c}: {m}')


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_comment(cat, name, timesmp, content): 
    m = Comment.objects.get_or_create(category=cat, username=name, timesmp=timesmp)[0]
    m.username = name
    m.timesmp = timesmp
    m.content = content
    m.save()
    return m
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    