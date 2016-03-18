from django.test import TestCase


#Tests for views

             
from django.core.urlresolvers import reverse


class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])


    from healthApp.models import Category

    def add_cat(name, views):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.save()
        return c


    def test_index_view_with_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """

        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)

#------------------------------------------------------------------------

#tests for models

#Test for Category

from healthApp.models import Category

class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        
        """
                ensure_views_are_positive should results True for categories where views are zero or positive
        """
        cat = Category(name='test',views=-1)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
            
        cat = Category('Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
#test for add page

import datetime
from django.utils import timezone

from healthApp.models import Page

class QuestionMethodTests(TestCase):

    def test_was_added_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_page = Page(pub_date=time)
        self.assertEqual(future_page.was_published_recently(), False)


#--------------------------------------------------------------------------

import unittest


#test three string methods
class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

if __name__ == '__main__':
    unittest.main()






        
