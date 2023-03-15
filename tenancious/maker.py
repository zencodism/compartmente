import copy
from django.db import connections, models
from django.apps import apps
from django.db import connection

class LabeledModel(models.Model):
    class Meta:
        abstract=True

    def __str__(self):
        return f"{self.name} [{type(self).__name__}]"

def create_model(
    name, parent, label="tenancious", target=None, options=None, admin_opts=None
):

    table_name = f"{label}_{name}".lower()

    try:
        model = apps.get_registered_model(label, name)
        return model
    except LookupError:
        pass

    name_parts = name.split('_')

    class Meta:
        db_table = table_name
        managed = False
        app_label = label
        verbose_name = f"{name_parts[1]} [{name_parts[0]}]"
        verbose_name_plural = f"{name_parts[1]}s [{name_parts[0]}]"

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {"__module__": f"{label}.models", "Meta": Meta}

    for field in parent._meta.fields:
        if field.name == 'id' or field.name in attrs:
            continue
        if isinstance(field, models.AutoField):
            attrs[field.name] = models.IntegerField(db_index=True, editable=False)
        else:
            attrs[field.name] = copy.copy(field)
            attrs[field.name]._unique = False
            attrs[field.name].primary_key = False
            if isinstance(field, models.ForeignKey):
                rel = copy.copy(field.remote_field)
                rel.related_name = '_rev_' + str(rel.related_query_name) or ''
                rel.model = target
                attrs[field.name].remote_field = rel

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (LabeledModel,), attrs)

    conn = connections["default"]
    editor = conn.schema_editor()
    editor.deferred_sql = []
    try:
        editor.create_model(model)
    except Exception as e:
        print("Sith happened", e)

    return model
