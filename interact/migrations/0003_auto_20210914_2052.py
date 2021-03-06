# Generated by Django 3.1.4 on 2021-09-14 12:52

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('interact', '0002_auto_20210914_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='attrs',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='database',
            name='trained_models',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='explore',
            name='records',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
