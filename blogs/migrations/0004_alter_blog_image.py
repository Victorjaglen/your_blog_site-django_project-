# Generated by Django 5.1.4 on 2024-12-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='fallback.jpeg', upload_to=''),
        ),
    ]
