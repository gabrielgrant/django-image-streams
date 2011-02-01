import re
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
py_identifier_re = re.compile(r'^[a-zA-Z_][\w]*$')

class ImageStream(object):
	number = 10
	app_label=''
	def __init__(self, name, registry):
		'''
		app_label defaults to the name of the app containing the model
		if app_label is None, the image stream will be in the global namespace
		'''
		if self.app_label == '':
			self.app_label = self.get_queryset().model._meta.module_name
		self.name = name
		self.registry = registry
	
	def get_queryset(self):
		if hasattr(self, 'queryset'):
			return self.queryset
		elif hasattr(self, 'model'):
			return self.model.objects.all()
		else:
			raise RuntimeError('either model or queryset must be specified')
	def filter_queryset(self, qs):
		return qs
	def get_filtered_queryset(self):
		return self.filter_queryset(self.get_queryset())
	def get_images(self):
		qs = self.get_filtered_queryset()
		return qs.values_list(self.field_name, flat=True)

class ImageStreamRegistry(object):
	def __init__(self, name=None):
		if name is not None and py_identifier_re.match(name) is None:
			raise ValueError('name must be a valid Python identifier')
		self.name = name
		self._registry = {} # stream_identifier -> stream_class instance
	
	def register(self, name, stream_class=None, **options):
		if app_label is not None and py_identifier_re.match(app_label) is None:
			raise ValueError('app_label must be a valid Python identifier')
		if py_identifier_re.match(name) is None:
			raise ValueError('name must be a valid Python identifier')
		_register(self, name, stream_class=None, **options)
		
	def _register(self, name, stream_class=None, **options):
		'''
		do registration without error checking, allowing us to register
		
		'''
		if stream_class is None:
			stream_class = ImageStream
		
		# If we got **options then dynamically construct a subclass of
		# stream_class with those **options.
		if options:
			# For reasons I don't quite understand, without a __module__
			# the created class appears to "live" in the wrong place,
			# which causes issues later on.
			options['__module__'] = __name__
			class_name = str("%sStream" % name)  # Python 2.x needs str
			stream_class = type(class_name, (stream_class,), options)
		stream_instance = stream_class(name, self)
		
		if stream_instance.app_label is None:
			key = name
		else:
			key = '%s:%s' % (stream_instance.app_label, name)
		self._registry[key] = stream_instance
	
	def fetch_stream(self, key):
		if key not in self._registry:
			# try to retrieve the object, and add it to the registry
			app_label, model_name, field_name = key.split('.')
			kwargs = {'field_name': field_name}
			kwargs['model'] = ContentType.objects.get(
				app_label=app_label, model=model_name
			).model_class()
			# register globally, *not* within the app label namespace
			self._register(name=key, registry=self, app_label=None, **kwargs)
		return self._registry[key]

registry = ImageStreamRegistry()

