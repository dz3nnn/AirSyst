from pyexpat import model
from django.db import models
from django.core.validators import FileExtensionValidator


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


class Brand(models.Model):
    """ Бренд """
    name = models.CharField(
        max_length=200, verbose_name='Название')
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Страна', null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Company(models.Model):
    """ Компании """
    name = models.CharField(
        max_length=200, verbose_name='Название')
    logo = models.ImageField(upload_to='company_logos/',
                             verbose_name='Логотип', null=True, blank=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


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


class Certificate(models.Model):
    """ Сертификаты """
    description = models.CharField(
        max_length=50, verbose_name='Описание', null=True, blank=True)
    pdf_file = models.FileField(
        upload_to='review_files/', verbose_name='Файл отзыва', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'


class PartType(models.Model):
    """ Тип запчасти """
    name = models.CharField(
        max_length=50, verbose_name='Название')
    image = models.ImageField(upload_to='part_type_images/',
                              verbose_name='Изображение', null=True, blank=True)

    # На данном этапе тут же наполнение?

    class Meta:
        verbose_name = 'Тип запчасти'
        verbose_name_plural = 'Типы запчастей'


class EquipmentCategory(models.Model):
    """ Категория оборудования """
    name = models.CharField(
        max_length=50, verbose_name='Название')
    image = models.ImageField(upload_to='equipment_category_images/',
                              verbose_name='Изображение', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория оборудования'
        verbose_name_plural = 'Категории оборудования'


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
    # Описание больше?
    description = models.CharField(
        max_length=600, verbose_name='Описание')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Project_Image(models.Model):
    """Галерея проекта """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Проект')
    image = models.ImageField(upload_to='project_images/',
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение проекта'
        verbose_name_plural = 'Изображения проекта'


class Equipment_Item(models.Model):
    """ Оборудование """
    pass

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


# ToDo
class Info(models.Model):
    """ Информация """
    pass


class Option(models.Model):
    """ Характеристика """
    pass

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class OptionValue(models.Model):
    """ Значение характеристики """
    pass

    class Meta:
        verbose_name = 'Значение арактеристики'
        verbose_name_plural = 'Значения арактеристики'


class OptionRelation(models.Model):
    """ Связь характеристик """
    pass

    class Meta:
        verbose_name = 'Связь характеристик'
        verbose_name_plural = 'Связи арактеристик'
