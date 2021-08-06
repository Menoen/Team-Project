from django.test import TestCase
from rango.models import Comment, Category
from django.contrib.auth.models import User


# Create your tests here.
# class ModelsTests(TestCase):
#     def test_ensure_views_are_positive(self):
#         """
#         Ensures the number of views received for a Category are positive or zero.
#         """
#
#     category = Category(name='test', views=-1, likes=0)
#     category.save()
#
#
#     def test_ensure_add_comments(self):
#         user = User(username='test2')
#         user.save()
#         category = Category(name='test')
#         category.save()
#         comment = Comment(category=category, username=user.username,content='This is test for comments')
#         comment.save()
#
#         print('test2 performed')
#         self.assertEqual(comment.username, 'test2')


class ModelTests(TestCase):

    def setEnvironment(self):
        try:
            from populate_rango import populate
            populate()
            print('set success')
            for category in Category.objects.all(self):
                print(category.name)
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Unknown error!')

    def get_category(self, name):

        from rango.models import Category
        try:
            self.setEnvironment()
            cat = Category.objects.get(name=name)
            print('success')
        except Category.DoesNotExist:
            cat = None
            print('fail')
        return cat

    def test_python_category_added(self):
        self.setEnvironment()
        cat = self.get_category('Python')
        self.assertIsNotNone(cat)

    def test_python_category_views(self):
        self.setEnvironment()
        cat = self.get_category('Python')
        self.assertEquals(cat.views, 128)

    def test_python_category_likes(self):
        self.setEnvironment()
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)
    def test_python_category_comments(self):
        self.setEnvironment()
        cat = self.get_category('Python')
        comment = cat.comment_set.count()
        self.assertEquals(comment, 2)
