from django.shortcuts import render
from django.contrib import messages

# Site views


def index(request):
    """ Index page view """
    context = {}
    # messages.add_message(request, messages.DEBUG, 'check')
    return render(request, 'site/index.html', context)


def about(request):
    """ About company view """
    context = {}
    return render(request, 'site/about.html', context)


def projects(request):
    """ Projects view """
    context = {}
    return render(request, 'site/projects.html', context)


def certificates(request):
    """ Certificates view """
    context = {}
    return render(request, 'site/certificates.html', context)


def contacts(request):
    """ Contacts view """
    context = {}
    return render(request, 'site/contacts.html', context)


def cart(request):
    """ Shopping cart view """
    context = {}
    return render(request, 'site/shopping-cart.html', context)


def order(request):
    """ Order view """
    context = {}
    return render(request, 'site/order.html', context)


def service_center(request):
    """ Service Center view """
    context = {}
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
    """ ?? """
    context = {}
    return render(request, 'site/equipment.html', context)


def product_card(request):
    """ ?? """
    context = {}
    return render(request, 'site/product-card.html', context)


def project_single(request):
    """ ?? """
    context = {}
    return render(request, 'site/project-singl.html', context)


def reviews(request):
    """ ?? """
    context = {}
    return render(request, 'site/reviews.html', context)


def spare_parts_next(request):
    """ ?? """
    context = {}
    return render(request, 'site/spare-parts-next.html', context)


def spare_parts_single(request):
    """ ?? """
    context = {}
    return render(request, 'site/spare-parts-singl.html', context)


def spare_parts(request):
    """ ?? """
    context = {}
    return render(request, 'site/spare-parts.html', context)
