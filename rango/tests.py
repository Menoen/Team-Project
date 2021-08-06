from django.test import TestCase
from rango.models import Comment, Category, Page
from populate_rango import populate
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class ModelTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')

    def get_category(self, name):

        from rango.models import Category
        try:
            self.setUp()
            cat = Category.objects.get(name=name)
            print('success')
        except Category.DoesNotExist:
            cat = None
            print('fail')
        return cat

    def test_category_added(self):
        cat = self.get_category('Python')
        self.assertIsNotNone(cat)

    def test_category_views(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.views, 128)

    def test_category_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)

    def test_category_comments(self):
        cat = self.get_category('Python')
        comment = cat.comment_set.count()
        self.assertEquals(comment, 2)
    def test_slug_name_work(self):
        category = Category(name="test for slug")
        category.save()
        self.assertEquals(category.slug, 'test-for-slug')

class ViewTests(TestCase):
    def setUp(self):
        populate()


    def test_Index_View(self):
        self.response = self.client.get(reverse('rango:index'))
        self.content = self.response.content.decode()

        self.assertIn('Rango says ...', self.content)
        self.assertTemplateUsed(self.response, 'rango/index.html')
        self.assertIn(b'img src="/static/images/rango.jpg', self.response.content)
        self.assertIn(b'<title>', self.response.content)
        self.assertIn(b'</title>', self.response.content)

    def test_About_View(self):
        self.response = self.client.get(reverse('rango:about'))
        self.content = self.response.content.decode()

        self.assertIn(b'img src="/media/cat.jpg', self.response.content)
        self.assertTemplateUsed(self.response, 'rango/about.html')

class FuncTests(TestCase):
    def setUp(self):
        populate()
        user = User.objects.create_user(username='testbot', email='test@test.com', password='abcabcabc123')
        user.save()

    def test_add_category_work(self):
        content = self.client.get(reverse('rango:index')).content.decode()

        self.assertTrue(reverse('rango:add_category') not in content)

        self.client.login(username='testbot', password='abcabcabc123')
        content = self.client.get(reverse('rango:index')).content.decode()

        self.assertTrue(reverse('rango:add_category') in content)

        self.client.post(reverse('rango:add_category'),
                         {'name': 'tests', 'views': 10, 'likes': 2})

        categories = Category.objects.filter(name='tests')
        self.assertEqual(len(categories), 1)




