# Generated by Django 5.0.6 on 2024-06-20 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printhub_app', '0003_alter_shoprate_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestFile',
            fields=[
                ('test_file_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='test_uploads/')),
            ],
        ),
    ]
