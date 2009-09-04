from django.db.models.base import ModelBase as dmodel
from django.conf import settings
from django.core.management.base import NoArgsCommand

apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django.')]

managed_models = []
for app in apps:
    exec 'import ' + app + '.models as models_module'
    models = [m for m in dir(models_module) if not m.startswith('__')]
    for model in models:
        try:
            model_class_obj = eval('models_module.' + model)
            if type(model_class_obj) == dmodel:
                if hasattr(model_class_obj(), 'translation'):
                    managed_models.append(model_class_obj)
        except (ImportError, NameError):
            pass

for model in managed_models:
    objs = model.objects.filter(translation__isnull=False)
    for obj in objs:
        tobj = obj.translation
        if not tobj.translation:
            tobj.translation = obj
            tobj.save()
            print "Normalized translation for: %s (%s | id: %d)" % (tobj, model,  tobj.pk)


class Command(NoArgsCommand):
    help = "Automatically normalizes translation relationships between objects"
    requires_model_validation = False

    def handle_noargs(self, **options):
        pass
