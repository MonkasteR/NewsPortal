# Generated by Django 4.2.4 on 2023-08-28 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('News', '0004_remove_subscriber_categories_subscriber_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='categories', to='News.subscriber'),
        ),
    ]
