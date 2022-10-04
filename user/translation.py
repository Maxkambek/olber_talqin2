from modeltranslation.translator import translator, TranslationOptions

from cargo.models import Cargo

class CargoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Cargo, CargoTranslationOptions)