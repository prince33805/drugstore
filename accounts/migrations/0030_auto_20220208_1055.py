# Generated by Django 3.2.6 on 2022-02-08 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='qty_front',
        ),
        migrations.RemoveField(
            model_name='medicine',
            name='qty_instock',
        ),
        migrations.RemoveField(
            model_name='medicine',
            name='qty_online',
        ),
        migrations.AddField(
            model_name='medicine',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='medicine',
            name='tags',
            field=models.ManyToManyField(to='accounts.Tag'),
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]