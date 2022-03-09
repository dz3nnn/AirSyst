from pyexpat import model
from django.db import models
from django.core.validators import FileExtensionValidator
from pdf2image import convert_from_path
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.conf import settings
from . import helps
from tinymce.models import HTMLField

# from ckeditor_uploader.fields import RichTextUploadingField


SERVICE_CHOICES = (
    ('MAINTENANCE', 'Обслуживание'),
    ('REPAIR', 'Сервис'),
)


class Country(models.Model):
    """ Страна для бренда """
    name = models.CharField(max_length=200, verbose_name='Название')
    flag = models.ImageField(upload_to='country_flags/',
                             verbose_name='Флаг', null=True, blank=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Brand(models.Model):
    """ Бренд """
    name = models.CharField(
        max_length=200, verbose_name='Название')
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Страна', null=True, blank=True)
    logo = models.FileField(upload_to='brand_logos/',
                            verbose_name='Логотип', null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Company(models.Model):
    """ Компании """
    name = models.CharField(
        max_length=200, verbose_name='Название')
    logo = models.ImageField(upload_to='company_logos/',
                             verbose_name='Логотип', null=True, blank=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name


class Review(models.Model):
    """ Отзывы """
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name='Организация')
    review_type = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, verbose_name='Вид работ', null=True, blank=True)
    description = models.CharField(
        max_length=400, verbose_name='Описание', null=True, blank=True)
    pdf_file = models.FileField(
        upload_to='review_files/', verbose_name='Файл отзыва', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return u"%s - %s" % (self.company.name, self.get_review_type_display())


class Certificate(models.Model):
    """ Сертификаты """
    description = models.CharField(
        max_length=50, verbose_name='Описание', null=True, blank=True)
    pdf_file = models.FileField(
        upload_to='review_files/', verbose_name='Файл отзыва', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)
    image = models.ImageField(
        upload_to='review_images/', verbose_name='Изображение', null=True, blank=True)

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return u"%s" % (self.description)


def convert_pdf_to_image(sender, instance, created, **kwargs):
    if created:
        instance.image = helps.get_path_for_pdf(
            'review_images/', 'jpg', instance.pdf_file)

        instance.save()


post_save.connect(convert_pdf_to_image, sender=Certificate)


class PartType(models.Model):
    """ Тип запчасти """
    name = models.CharField(
        max_length=50, verbose_name='Название')
    image = models.FileField(upload_to='part_type_files/',
                             verbose_name='Изображение', null=True, blank=True)

    # На данном этапе тут же наполнение?

    class Meta:
        verbose_name = 'Тип запчасти'
        verbose_name_plural = 'Типы запчастей'

    def __str__(self):
        return u"%s" % (self.name)


class EquipmentCategory(models.Model):
    """ Категория оборудования """
    name = models.CharField(
        max_length=50, verbose_name='Название')
    image = models.ImageField(upload_to='equipment_category_images/',
                              verbose_name='Изображение', null=True, blank=True)
    single_page = models.BooleanField(
        verbose_name='Без каталога', default=False)
    description = HTMLField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория оборудования'
        verbose_name_plural = 'Категории оборудования'

    def __str__(self):
        return u"%s" % (self.name)


class EquipmentSubCategory(models.Model):
    """ Подкатегория оборудования """
    category = models.ForeignKey(
        EquipmentCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(
        max_length=50, verbose_name='Название')
    image = models.ImageField(upload_to='equipment_sub_category_images/',
                              verbose_name='Изображение', null=True, blank=True)

    class Meta:
        verbose_name = 'Подкатегория оборудования'
        verbose_name_plural = 'Подкатегории оборудования'

    def __str__(self):
        return u"%s - %s" % (self.category.name, self.name)


class Project(models.Model):
    """ Проекты """
    project_type = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, verbose_name='Вид работ', null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    date = models.DateField(verbose_name='Дата')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name='Организация')
    title = models.CharField(
        max_length=250, verbose_name='Заголовок')
    description = HTMLField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return u"%s - %s (№%s)" % (self.get_project_type_display(), self.company.name, self.pk)


class Project_Image(models.Model):
    """Галерея проекта """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Проект')
    image = models.ImageField(upload_to='project_images/',
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение проекта'
        verbose_name_plural = 'Изображения проекта'

    def __str__(self):
        return u"изображение (id:%s)" % (self.pk)


class Equipment_Item(models.Model):
    """ Оборудование """
    name = models.CharField(
        max_length=100, verbose_name='Название', null=True)
    category = models.ForeignKey(
        EquipmentCategory, on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True)
    sub_category = models.ForeignKey(
        EquipmentSubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория', null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Бренд', null=True, blank=True)
    country_create = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Страна изготовителя', null=True, blank=True)
    article = models.IntegerField(
        verbose_name='Артикул', null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена', null=True, blank=True)
    delivery_time = models.CharField(
        max_length=100, verbose_name='Срок доставки', null=True, blank=True)
    supply_time = models.CharField(
        max_length=100, verbose_name='Срок поставки', null=True, blank=True)
    warranty = models.CharField(
        max_length=100, verbose_name='Гарантия', null=True, blank=True)
    certificate = models.ForeignKey(
        Certificate, on_delete=models.CASCADE, verbose_name='Сертификат', null=True, blank=True)

    weight = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Вес (кг)', null=True, blank=True)
    width = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Ширина (см)', null=True, blank=True)
    length = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Длина (см)', null=True, blank=True)
    height = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Высота (см)', null=True, blank=True)

    # ck_check = RichTextUploadingField(verbose_name='Наполнение (тест)', null=True, blank=True)

    description = HTMLField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

    def __str__(self):
        return u"%s (art:%s)" % (self.name, self.article)


class Equipment_Image(models.Model):
    """Галерея оборудования """
    equip = models.ForeignKey(
        Equipment_Item, on_delete=models.CASCADE, verbose_name='Проект')
    image = models.ImageField(upload_to='equip_images/',
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение оборудования'
        verbose_name_plural = 'Изображения оборудования'

    def __str__(self):
        return u"изображение (id:%s)" % (self.pk)


class Option(models.Model):
    """ Характеристика """
    name = models.CharField(
        max_length=100, verbose_name='Характеристика', null=True, blank=True)
    numerical = models.BooleanField(verbose_name='Числовое', default=False)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return u"%s" % (self.name)


class OptionValue(models.Model):
    """ Значение характеристики """
    name = models.CharField(
        max_length=100, verbose_name='Значение', null=True, blank=True)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристики'

    def __str__(self):
        return u"%s" % (self.name)


class OptionRelation(models.Model):
    """ Связь характеристик """
    equipment = models.ForeignKey(
        Equipment_Item, on_delete=models.CASCADE, verbose_name='Оборудование', null=True, blank=True)
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE, verbose_name='Характеристика', null=True, blank=True)
    option_value = models.ForeignKey(
        OptionValue, on_delete=models.CASCADE, verbose_name='Значение', null=True, blank=True)

    class Meta:
        verbose_name = 'Связь характеристик'
        verbose_name_plural = 'Связи арактеристик'

    def __str__(self):
        return u"%s(%s - %s)" % (self.equipment.name, self.option.name, self.option_value.name)


class Info(models.Model):
    """ Информация """
    name = models.CharField(
        max_length=100, verbose_name='Название', null=True, blank=True)
    content = HTMLField(verbose_name='Значение', null=True, blank=True)

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информация'

    def __str__(self):
        return u"%s (id:%s)" % (self.name, self.pk)


class Worker(models.Model):
    """ Сотрудники """
    name = models.CharField(
        max_length=100, verbose_name='Имя (описание)', null=True, blank=True)
    position = models.CharField(
        max_length=100, verbose_name='Должность', null=True, blank=True)
    image = models.ImageField(upload_to='worker_image/',
                              verbose_name='Изображение')
    content = HTMLField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return u"%s (id:%s)" % (self.name, self.pk)
