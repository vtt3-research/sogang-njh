from django import template

register = template.Library()


@register.inclusion_tag('WebLabeler/base_nav.html', takes_context=True)
def nav_bar(context, passing_media=False, selected='Labeling'):
    if passing_media:
        return {
            'user': context['user'],
            'media': context['media'],
            'selected_name': selected,
        }
    else:
        return {
            'user': context['user'],
        }


@register.inclusion_tag('WebLabeler/media_info_header.html', takes_context=True)
def media_header(context):
    return {
        'media': context['media'],
        'info': context['info']
    }


@register.inclusion_tag('WebLabeler/util_getImage.html')
def util_get_image():
    return
