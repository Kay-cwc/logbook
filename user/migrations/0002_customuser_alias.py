# Generated by Django 3.0.5 on 2020-10-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='alias',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
