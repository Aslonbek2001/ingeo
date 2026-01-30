from modeltranslation.translator import register, TranslationOptions
from .models import Carousel, Collaborations

@register(Carousel)
class CarouselTranslationOptions(TranslationOptions):
    fields = ("title", "description")

@register(Collaborations)
class CollaborationsTranslationOptions(TranslationOptions):
    fields = ("title", )