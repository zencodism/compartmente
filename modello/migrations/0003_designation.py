# Generated by Django 4.1.7 on 2023-03-07 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modello', '0002_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('site', models.ManyToManyField(to='modello.site')),
            ],
        ),
    ]
