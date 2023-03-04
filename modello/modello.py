from django.contrib import admin
from django.db import connections, models
from django.apps import apps
from django.db import connection

def create_model(
    name, parent, label="modello", options=None, admin_opts=None
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

    # fields = {f.name: f for f in parent._meta.fields}
    # if fields:
    #     attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (parent,), attrs)

    conn = connections["default"]
    editor = conn.schema_editor()
    editor.deferred_sql = []
    try:
        editor.create_model(model)
    except Exception:
        pass

    admin.site.register(model)
    return model
