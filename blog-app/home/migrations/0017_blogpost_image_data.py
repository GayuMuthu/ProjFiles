# Generated by Django 4.2 on 2023-05-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_profile_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image_data',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
