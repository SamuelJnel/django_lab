# Generated by Django 3.2.8 on 2021-10-22 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20211022_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='chinchilla',
            name='toys',
            field=models.ManyToManyField(to='main_app.Toy'),
        ),
    ]
