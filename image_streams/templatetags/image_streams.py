from django import template
from .. import registry

register = template.Library()

@register.inclusion_tag('image_streams/image_stream.html')
def image_stream(stream_key, number=None,
	img_attr='', title_attr='', link_attr=''
):
	if ':' in stream_key:
		stream = registry.fetch_stream(stream_key)
		img_attr, title_attr, link_attr = stream.get_attrs()
	else:
		stream = registry.fetch_stream('.'.join([stream_key,img_attr]))
	if number is not None:
		number = int(number)
	else:
		number = stream.number
	src_attr = img_attr + '.url'
	attrs = src_attr, title_attr, link_attr
	attrs = [('img.%s' % attr if attr else '') for attr in attrs]
	ctx = dict(zip(['src', 'title', 'link'], attrs))
	qs = stream.get_filtered_queryset()
	# django blows up if we try to access a null image, so filter them out
	# see: https://code.djangoproject.com/ticket/13327 or
	# http://groups.google.com/group/django-users/browse_frm/thread/471162ba4e515311
	qs = qs.exclude(**{img_attr.replace('.', '__'): ''})  # filter nulls
	ctx['images'] = qs.order_by('?')[:number]  # randomly ordered images
	return ctx


