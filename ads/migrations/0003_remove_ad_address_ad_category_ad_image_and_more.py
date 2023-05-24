# Generated by Django 4.2.1 on 2023-05-23 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('ads', '0002_alter_ad_options_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='address',
        ),
        migrations.AddField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ads.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ad_images'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
