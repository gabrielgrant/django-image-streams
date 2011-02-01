from django import template
from .. import registry

register = template.Library()

@register.inclusion_tag('image_streams/image_stream.html')
def image_stream(stream_key, number=None):
	stream = registry.fetch_stream(stream_key)
	if number is not None:
		number = int(number)
	else:
		number = stream.number
	qs = stream.get_filtered_queryset()
	return {'images':qs.order_by('?')[:number]}  # randomly ordered images


