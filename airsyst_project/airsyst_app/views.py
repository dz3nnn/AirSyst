from email.policy import default
from urllib import request
from django.shortcuts import render
from django.contrib import messages
from .models import *
from .helps import *
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import re
from .templatetags.app_tags import *
import json
from django.http import JsonResponse
import requests

# Helps


def json_return(message):
    """Сниппет для JSON ответа"""
    return JsonResponse({
        'message': message
    })


def get_brands_for_equip(equips):
    """ Get Brands for equip list """
    brand_ids = equips.values_list('brand__pk', flat=True)
    brands = Brand.objects.filter(pk__in=brand_ids)
    return brands


def get_options_for_equip(equips):
    """ Get Options for equip list """
    equip_ids = equips.values_list('pk', flat=True)
    options = OptionRelation.objects.filter(
        equipment__pk__in=equip_ids)
    return options


def get_options_by_relations(option_relations):
    relation_ids = option_relations.values_list('option__pk', flat=True)
    options_list = Option.objects.filter(
        pk__in=relation_ids).order_by('name')
    return options_list


def apply_filter_for_equip(request, equips):
    """ Apply filters to Equipment QuerySet """
    brand_ids_from_req = get_brands_from_params_v2(request)

    # Apply brands
    if(brand_ids_from_req):
        equips = equips.filter(brand__in=brand_ids_from_req)

    # Apply filters
    option_ids = get_numeric_parameters_from_request(request)
    for option_id in option_ids:
        option_values_string = request.GET.get(option_id)
        if(option_values_string):

            equips_ids = equips.values_list('pk', flat=True)

            option_values_string = re.sub(
                '[^0-9:,.]', '', option_values_string)

            option_model = Option.objects.filter(pk=option_id).first()

            if option_model.numerical:
                # param is 100:800
                option_values = option_values_string.split(':')
                # Maybe check if option_values len > 1
                float_values = to_float(option_values)
                min_val = min(float_values, default=0)
                max_val = max(float_values, default=0)

                relations = OptionRelation.objects.filter(
                    equipment__pk__in=equips_ids, option__pk=option_id).distinct()

                new_ids = []
                for rel in relations:
                    z = rel.option_value.name.replace(',', '.')
                    if is_float(z):
                        z = float(z)
                        if z >= min_val and z <= max_val:
                            new_ids.append(rel.pk)

                relations_ids = OptionRelation.objects.filter(
                    equipment__pk__in=equips_ids, option__pk=option_id, pk__in=new_ids).values_list('equipment__pk', flat=True).distinct()
                equips = Equipment_Item.objects.filter(
                    pk__in=relations_ids)
            else:
                # param is 1:2:3
                option_values_ids = option_values_string.split(':')
                option_values_ids_formatted = [
                    x.replace('/', '') for x in option_values_ids]
                equips_ids_filter = OptionRelation.objects.filter(
                    equipment__pk__in=equips_ids, option_value__pk__in=option_values_ids_formatted, option__pk=option_id).values_list('equipment__pk', flat=True)
                equips = Equipment_Item.objects.filter(
                    pk__in=equips_ids_filter)
    return equips


def get_numeric_parameters_from_request(request):
    params = []
    if request.GET:
        check = request.GET
        for t in check:
            if t.isnumeric():
                params.append(t)
    return params


def get_brands_from_params(request):
    """ Brands from GET """
    brands_request = request.GET.get('brands')
    if brands_request:
        brand_items_from_request = brands_request.split(';')
        add_debug_msg(request, brands_request)
        return brand_items_from_request
    return None


def get_brands_from_params_v2(request):
    """ Brands from GET """
    brands_request = request.GET.get('brands')
    if brands_request:
        brands_request = re.sub('[^0-9:]', '', brands_request)
        brand_items_from_request = brands_request.split(':')
        return brand_items_from_request
    return None


# Site views


def add_debug_msg(request, msg):
    messages.add_message(request, messages.DEBUG, msg)


def view_404(request, exception):
    return render(request, 'site/404.html')


def index(request):
    """ Index page view """
    context = {
        'all_brands': Brand.objects.all(),
    }
    return render(request, 'site/index.html', context)


def about(request):
    """ About company view """
    context = {}
    return render(request, 'site/about.html', context)


def projects(request):
    """ Projects view """
    page_filter = request.GET.get('filter')
    if page_filter:
        projects = Project.objects.filter(project_type=page_filter)
    else:
        projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'site/projects.html', context)


def certificates(request):
    """ Certificates view """
    context = {}
    return render(request, 'site/certificates.html', context)


def contacts(request):
    """ Contacts view """
    context = {}
    return render(request, 'site/contacts.html', context)


class BasketItem():
    def __init__(self, product_id, count):
        self.product_id = product_id
        self.count = count
        self.equip_obj = Equipment_Item.objects.filter(pk=product_id).first()
        self.full_price = self.equip_obj.price * self.count


def get_basket_items_from_cookie(request):
    basket = request.COOKIES.get('shopping-cart')
    if basket:
        basket_cookie = json.loads(basket)
        items = []
        for basket_item in basket_cookie:
            product_id = basket_item['id']
            count = basket_item['count']
            if product_id and count:
                item_to_add = BasketItem(
                    product_id=int(product_id), count=int(count))
                items.append(item_to_add)
        return items
    else:
        return None


def cart(request):
    """ Shopping cart view """

    basket_items = get_basket_items_from_cookie(request)

    if basket_items:
        pass

    context = {
        'basket_items': basket_items
    }
    return render(request, 'site/shopping-cart.html', context)


def order(request):
    """ Order view """
    context = {}
    return render(request, 'site/order.html', context)


def service_center(request):
    """ Service Center view """

    # Load 5 results?

    page_filter = request.GET.get('filter')
    if page_filter:
        pass
    else:
        projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'site/service-center.html', context)


def air_treatment(request):
    """ ?? """
    context = {}
    return render(request, 'site/air-treatment.html', context)


def catalog(request):
    """ ?? """
    context = {}
    return render(request, 'site/catalog.html', context)


def equipment(request):
    """ All Equipment categories Page """
    categories = EquipmentCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'site/equipment.html', context)


def equipment_by_category(request, category_id):
    """ Find context for Category """
    category = get_object_or_404(EquipmentCategory, pk=category_id)
    sub_categories = EquipmentSubCategory.objects.filter(
        category__pk=category_id)
    context = {
        'current_category': category
    }
    # Single > Subcategories > Catalog
    # Is Single? > Render single page
    if category.single_page:
        # render single
        n2_cat_id = 4
        o2_cat_id = 5
        if category_id == n2_cat_id:
            return render(request, 'site/gen-n2.html', context)
        if category_id == o2_cat_id:
            return render(request, 'site/gen-o2.html', context)
    elif sub_categories:
        context.update(
            {
                'sub_categories': sub_categories,
            }
        )
        return render(request, 'site/air-treatment.html', context)
    else:
        return redirect(equipment_catalog_by_category, category_id)

# Catalogs


def equipment_catalog_by_sub_category(request, sub_category_id):
    """ Get Catalog for SubCategory"""
    sub_category = get_object_or_404(EquipmentSubCategory, pk=sub_category_id)
    category = get_object_or_404(
        EquipmentCategory, pk=sub_category.category.pk)
    context = {
        'main_category': category,
        'category': sub_category,
    }
    return render(request, 'site/catalog.html', context)


def equipment_catalog_by_category(request, category_id):
    """ Get Catalog for Category"""
    category = get_object_or_404(EquipmentCategory, pk=category_id)
    items = Equipment_Item.objects.filter(category__pk=category_id)

    brands = get_brands_for_equip(items)
    options_relations = get_options_for_equip(items)

    items = apply_filter_for_equip(request, items)

    # options is Option Model
    options = get_options_by_relations(options_relations)

    context = {
        'category': category,
        'items': items,
        'brands': brands,
        'options': options,
    }
    return render(request, 'site/catalog.html', context)


def equipment_single(request, product_id):
    """ Single Equipment Page (Product Card) """
    item = get_object_or_404(Equipment_Item, pk=product_id)
    images = Equipment_Image.objects.filter(equip__pk=product_id)
    options = OptionRelation.objects.filter(equipment__pk=product_id)
    context = {
        'item': item,
        'images': images,
        'options': options
    }
    return render(request, 'site/product-card.html', context)


def product_card(request):
    """ ?? """
    context = {}
    return render(request, 'site/product-card.html', context)


def project_single(request, project_id):
    """ Page for project by id """
    project = get_object_or_404(Project, pk=project_id)
    projects_images = Project_Image.objects.filter(project__pk=project_id)
    context = {
        'project': project,
        'images': projects_images
    }
    return render(request, 'site/project-singl.html', context)


def reviews(request):
    """ ?? """
    context = {}
    return render(request, 'site/reviews.html', context)


def spare_parts_next(request):
    """ PartTypes  """
    context = {
        'part_types': PartType.objects.all()
    }
    return render(request, 'site/spare-parts-next.html', context)


def spare_parts_single(request):
    """ ?? """
    context = {}
    return render(request, 'site/spare-parts-singl.html', context)


def spare_parts(request):
    """ Brands for parts """
    context = {
        'all_brands': Brand.objects.all()
    }
    return render(request, 'site/spare-parts.html', context)


def send_feedback(request):
    """ Send feedback for call """
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        if email:

            text = u'Имя: %s\nEmail: %s\nСообщение: %s' % (name, email, msg)
            result = send_to_telegram(text)
            return result
        # Send to Mail
    return JsonResponse({
        'status_code': 0
    })


def send_basket(request):
    """ Send basket after order """
    if True:
        # name = request.POST.get('name')
        # get info
        basket_items = get_basket_items_from_cookie(request)
        if request.POST and basket_items:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if phone or email:
                items_text = u'Имя: %s\nEmail: %s\nТелефон: %s\n' % (
                    name, email, phone)
                counter = 1
                for item in basket_items:
                    items_text += u'%s. %s (кол-во: %s) (art: %s) (цена: %s BYN; итого: %s BYN)\n' % (
                        counter, item.equip_obj.name, item.count, item.equip_obj.article, item.equip_obj.price, item.full_price)
                    counter += 1
                items_text += u'\nОбщее количество: %s ед.\nОбщий вес: %s кг.\nОбщая стоимость: %s BYN' % (get_basket_full_count_func(
                    basket_items), get_basket_full_weight_func(basket_items), get_basket_full_price_func(basket_items))

                # text = u'Имя: %s\nEmail: %s\nСообщение: %s' % (name, email, msg)
                text = items_text

                result = send_to_telegram(text)
                return result
                # Send to Mail
    return JsonResponse({
        'status_code': 0
    })
