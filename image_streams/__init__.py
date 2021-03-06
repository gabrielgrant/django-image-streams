from django.conf import settings
from image_streams.stream_registry import registry
from django.contrib.contenttypes.models import ContentType

def register_from_settings():
	for name, kwargs in settings.IMAGE_STREAMS.iteritems():
		model = kwargs.get('model', None)
		if isinstance(model, basestring):
			app_label, model = model.split('.')
			kwargs['model'] = ContentType.objects.get(
				app_label=app_label, model=model
			).model_class()
		# register globally, *not* within the app label namespace
		registry.register(name=name, app_label=None, **kwargs)

