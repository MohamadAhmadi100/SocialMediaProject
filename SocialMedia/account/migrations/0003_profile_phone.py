# Generated by Django 3.1.7 on 2021-03-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210324_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.PositiveIntegerField(blank=True, max_length=12, null=True),
        ),
    ]