# Generated by Django 5.1.4 on 2025-02-11 08:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_remove_index_project_amount_paid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index_project',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='index_project',
            name='client_name',
        ),
        migrations.RemoveField(
            model_name='index_project',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='index_project',
            name='email',
        ),
        migrations.RemoveField(
            model_name='index_project',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='index_project',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='index_project',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='projects/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='index_project',
            name='link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='index_project',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='index_project',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='index_project',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='ProjectImage',
        ),
    ]
