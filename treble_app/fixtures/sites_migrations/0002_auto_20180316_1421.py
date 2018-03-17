# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def insert_sites(apps, schema_editor):
    """Populate the sites model"""
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().delete()

    # Register SITE_ID = 1
    Site.objects.create(domain='127.0.0.1:8000', name='default')
    # Register SITE_ID = 2
    Site.objects.create(domain='treble.pythonanywhere.com', name='pythonanywhere')


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_sites)
    ]