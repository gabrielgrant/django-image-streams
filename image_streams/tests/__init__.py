from django.test import TestCase

from image_streams.templatetags.image_streams import image_stream

from .models import Image

class ImageStreamTests(TestCase):
	def test_filter_null_images(self):
		""" Null images should be filtered out to avoid fireworks (or showing blanks) """
		i = Image.objects.create(title='myimage')
		ctx = image_stream('tests.image', number=3, img_attr='image', title_attr='title')
		self.assertEqual(ct['images'], [])
