from django.db import models

class Image(models.Model):
	title = models.CharField(max_length=200, blank=True)
	image = models.ImageField(max_length=200, upload_to='test_images', blank=True)
	def __unicode__(self):
		return '%s' % self.title
		
