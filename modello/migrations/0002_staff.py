# Generated by Django 4.1.7 on 2023-03-07 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modello.site')),
            ],
        ),
    ]
