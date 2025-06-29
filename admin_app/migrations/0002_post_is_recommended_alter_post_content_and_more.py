# Generated by Django 5.2 on 2025-06-17 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_recommended',
            field=models.BooleanField(default=False, help_text='Featured or recommended posts appear in a special section.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, help_text='The main content of the blog post, written in Markdown or HTML.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, help_text='A unique slug for the post URL.', max_length=250, unique_for_date='publish_date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('PL', 'Planned'), ('DF', 'Draft'), ('SC', 'Scheduled'), ('PB', 'Published')], default='PL', max_length=2),
        ),
    ]
