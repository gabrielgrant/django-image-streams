from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def resolve(context, name):
	if name:
		try:
			return template.Variable(name).resolve(context)
		except template.VariableDoesNotExist:
			pass
	return ''

