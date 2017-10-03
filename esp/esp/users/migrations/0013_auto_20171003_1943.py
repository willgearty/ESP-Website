# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20170927_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='event',
            field=models.CharField(max_length=80, choices=[(b'student_survey', b'Completed student survey'), (b'teacher_survey', b'Completed teacher survey'), (b'reg_confirmed', b'Confirmed registration'), (b'attended', b'Attended program'), (b'conf_email', b'Was sent confirmation email'), (b'teacher_quiz_done', b'Completed teacher quiz'), (b'paid', b'Paid for program'), (b'med', b'Submitted medical form'), (b'med_bypass', b'Recieved medical bypass'), (b'liab', b'Submitted liability form'), (b'onsite', b'Registered for program on-site'), (b'schedule_printed', b'Printed student schedule on-site'), (b'teacheracknowledgement', b'Did teacher acknowledgement'), (b'minorspolicyacknowledgement', b'Acknowledged minors policy'), (b'lunch_selected', b'Selected a lunch block'), (b'extra_form_done', b'Filled out Custom Form'), (b'extra_costs_done', b'Filled out Student Extra Costs Form'), (b'donation_done', b'Filled out Donation Form'), (b'waitlist', b'Waitlisted for a program'), (b'interview', b'Teacher-interviewed for a program'), (b'teacher_training', b'Attended teacher-training for a program'), (b'teacher_checked_in', b'Teacher checked in for teaching on the day of the program'), (b'twophase_reg_done', b'Completed two-phase registration')]),
        ),
    ]
