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
	ctx['images'] = qs.order_by('?')[:number]  # randomly ordered images
	return ctx


