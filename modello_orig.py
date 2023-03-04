from django.contrib import admin
from django.db import connections, models

from trees.models import Product


def create_model(
    name, fields=None, app_label="", module="", options=None, admin_opts=None
):
    """
    Create specified model
    """

    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, "app_label", app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {"__module__": module, "Meta": Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:

        class Admin(admin.ModelAdmin):
            pass

        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model


def modello_install(model):
    # from django.core.management import sql, color
    from django.db import connection

    # Standard syncdb expects models to be in reliable locations,
    # so dynamic models need to bypass django.core.management.syncdb.
    # On the plus side, this allows individual models to be installed
    # without installing the entire project structure.
    # On the other hand, this means that things like relationships and
    # indexes will have to be handled manually.
    # This installs only the basic table definition.
    # disable terminal colors in the sql statements
    # style = color.no_style()

    conn = connections["default"]
    editor = conn.schema_editor()
    editor.deferred_sql = []
    editor.create_model(model)
    # cursor = connection.cursor()
    # statements, pending = sql.sql_model_create(model, style)
    # for sql in statements:
    #     print(sql)
    #     cursor.execute(sql)


def modello_test():
    hmm = {f.name: f for f in Product._meta.fields}
    DummyProduct = create_model(
        "DummyProduct", fields=hmm, app_label="trees", module="trees.models"
    )
    modello_install(DummyProduct)
    print(DummyProduct.objects.count())
    print(DummyProduct._meta.fields)
