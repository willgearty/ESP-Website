# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0015_accountingmodule_autoschedulerfrontendmodule_bulkcreateaccountmodule_lotteryfrontendmodule'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinorsPolicyModule',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('modules.programmoduleobj',),
        ),
    ]
