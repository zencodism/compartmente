import copy
from django.db import connections, models
from django.apps import apps
from django.db import connection

def create_model(
    name, parent, label="modello", target=None, options=None, admin_opts=None
):

    table_name = f"{label}_{name}".lower()

    try:
        model = apps.get_registered_model(label, name)
        return model
    except LookupError:
        pass

    class Meta:
        db_table = table_name
        managed = False
        app_label = label

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {"__module__": f"{label}.models", "Meta": Meta}

    def strfun(self):
        return f"{self.name} [{name}]"
    attrs["__str__"] = strfun

    for field in parent._meta.fields:
        print(field)
        if field.name == 'id':
            continue
        #if field.attname in attrs:
        if field.name in attrs:
            raise ImproperlyConfigured
        if isinstance(field, models.AutoField):
            # Audit models have a separate AutoField
            attrs[field.name] = models.IntegerField(db_index=True, editable=False)
        else:
            attrs[field.name] = copy.copy(field)
            # If 'unique' is in there, we need to remove it, otherwise the index
            # is created and multiple audit entries for one item fail.
            attrs[field.name]._unique = False
            # If a model has primary_key = True, a second primary key would be
            # created in the audit model. Set primary_key to false.
            attrs[field.name].primary_key = False

            # Rebuild and replace the 'rel' object to avoid foreign key clashes.
            # Borrowed from the Basie project
            # Basie is MIT and GPL dual licensed.
            if isinstance(field, models.ForeignKey):
                rel = copy.copy(field.remote_field)
                rel.related_name = '_rev_' + str(rel.related_query_name) or ''
                rel.model = target
                attrs[field.name].remote_field = rel

    print("Hello world", attrs)
    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    conn = connections["default"]
    editor = conn.schema_editor()
    editor.deferred_sql = []
    try:
        editor.create_model(model)
    except Exception as e:
        print("Shit happened", e)

    return model
