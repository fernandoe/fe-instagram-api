# Generated by Django 2.1.3 on 2018-12-08 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0012_auto_20181208_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='identifier',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='identifier',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
