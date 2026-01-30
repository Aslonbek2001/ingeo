from modeltranslation.translator import register, TranslationOptions
from .models import Page, Menu, Employee, PageFiles

@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "description", "sub_title", "direction", "duration")

@register(Employee)
class PageTranslationOptions(TranslationOptions):
    fields = ("full_name", "position", "description")

@register(PageFiles)
class PageTranslationOptions(TranslationOptions):
    fields = ("title",)