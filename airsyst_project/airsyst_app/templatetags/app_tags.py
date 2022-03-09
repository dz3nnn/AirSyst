import datetime
from django import template
from airsyst_app.models import *
import re
from airsyst_app.helps import *

register = template.Library()

MONTHS = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря'
]


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def to_float(arr):
    result = []
    for t in arr:
        z = t.replace(',', '.')
        if is_float(z):
            result.append(float(z))
    return result


@register.filter
def get_day(value):
    """ Get day from date"""
    result = value.strftime('%d')
    if len(result) < 2:
        result = '0' + result
    return result


@register.filter
def trim_phone_for_tag(value):
    """ Trim all except + and numbers """
    return re.sub('[^0-9+]', '', value)


@register.filter
def get_month(value):
    """ Get month from date"""
    return MONTHS[value.month-1]


@register.filter
def get_year(value):
    """ Get year from date"""
    return value.year


@register.filter
def get_first_image_for_equip(value):
    image = Equipment_Image.objects.filter(equip__pk=value).first()
    return image.image.url


@register.simple_tag
def get_min_value_for_option(option_id, equips):
    equips_id = equips.values_list('pk', flat=True)
    relations = OptionRelation.objects.filter(
        equipment__pk__in=equips_id, option__pk=option_id).values_list('option_value_id', flat=True).distinct()
    opt_values = OptionValue.objects.filter(
        pk__in=relations).values_list('name', flat=True)
    float_values = to_float(opt_values)
    return min(float_values, default=0)


@register.simple_tag
def get_max_value_for_option(option_id, equips):
    equips_id = equips.values_list('pk', flat=True)
    relations = OptionRelation.objects.filter(
        equipment__pk__in=equips_id, option__pk=option_id).values_list('option_value_id', flat=True).distinct()
    opt_values = OptionValue.objects.filter(
        pk__in=relations).values_list('name', flat=True)
    float_values = to_float(opt_values)
    return max(float_values, default=0)


@register.simple_tag
def get_images_for_project(value):
    """ Get images for project"""
    image = Project_Image.objects.filter(project__pk=value).first()
    return image


@register.simple_tag
def get_option_values(equips, option_id):
    equips_id = equips.values_list('pk', flat=True)
    relations = OptionRelation.objects.filter(
        equipment__pk__in=equips_id, option__pk=option_id).values_list('option_value_id', flat=True).distinct()
    result = OptionValue.objects.filter(pk__in=relations).order_by('name')
    return result


@register.simple_tag
def get_info_value_by_pk(info_id):
    return Info.objects.filter(pk=info_id).first().content


@register.filter
def get_basket_full_count(items):
    return get_basket_full_count_func(items)


@register.filter
def get_basket_full_weight(items):
    return get_basket_full_weight_func(items)


@register.filter
def get_basket_full_price(items):
    return get_basket_full_price_func(items)
