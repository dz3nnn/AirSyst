from django.conf import settings
import os
from pdf2image import convert_from_path
from django.http import JsonResponse
import requests
from airsyst_project.config import *


def get_path_for_pdf(COVER_PAGE_DIRECTORY, COVER_PAGE_FORMAT, PDF_FILE):

    cover_page_dir = os.path.join(
        settings.MEDIA_ROOT, COVER_PAGE_DIRECTORY)

    if not os.path.exists(cover_page_dir):
        os.mkdir(cover_page_dir)

    cover_page_image = convert_from_path(
        pdf_path=PDF_FILE.path,
        dpi=200,
        first_page=1,
        last_page=1,
        fmt=COVER_PAGE_FORMAT,
        output_folder=cover_page_dir,
    )[0]

    pdf_filename, extension = os.path.splitext(
        os.path.basename(PDF_FILE.name))
    new_cover_page_path = '{}.{}'.format(os.path.join(
        cover_page_dir, pdf_filename), COVER_PAGE_FORMAT)
    # rename the file that was saved to be the same as the pdf file
    os.rename(cover_page_image.filename, new_cover_page_path)
    # get the relative path to the cover page to store in model
    new_cover_page_path_relative = '{}.{}'.format(os.path.join(
        COVER_PAGE_DIRECTORY, pdf_filename), COVER_PAGE_FORMAT)
    return new_cover_page_path_relative


def get_basket_full_count_func(items):
    result = 0
    if items:
        for t in items:
            if t.count:
                result = result + t.count
    return result


def get_basket_full_weight_func(items):
    result = 0
    if items:
        for t in items:
            if t.equip_obj.weight and t.count:
                result = result + (t.count * t.equip_obj.weight)
    return result


def get_basket_full_price_func(items):
    result = 0
    if items:
        for t in items:
            if t.equip_obj.price and t.count:
                result = result + (t.count * t.equip_obj.price)
    return result


def send_to_telegram(text):
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
    }
    response = requests.get(
        u'https://api.telegram.org/bot%s/sendMessage' % (TELEGRAM_BOT_TOKEN), params=payload)
    code = response.status_code
    return JsonResponse({
        'status_code': code
    })
