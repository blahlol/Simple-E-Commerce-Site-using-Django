# Generated by Django 3.1.1 on 2021-04-17 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='name',
            field=models.CharField(default='Karan', max_length=30),
            preserve_default=False,
        ),
    ]
