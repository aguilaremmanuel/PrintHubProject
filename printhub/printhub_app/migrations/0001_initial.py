# Generated by Django 4.2.13 on 2024-07-07 01:18

from django.db import migrations, models
import django.db.models.deletion
import printhub_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('shop_name', models.CharField(max_length=15)),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('contact_no', models.CharField(max_length=15)),
                ('date_registered', models.DateTimeField(blank=True, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('shop_status', models.CharField(default='open', max_length=15)),
            ],
            options={
                'db_table': 'shop_account',
            },
        ),
        migrations.CreateModel(
            name='ShopFolder',
            fields=[
                ('folder_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, default='hidden', max_length=10, null=True)),
                ('folder_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='printhub_app.shop')),
            ],
            options={
                'db_table': 'shop_folder',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('date_registered', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_account',
            },
        ),
        migrations.CreateModel(
            name='UserFolder',
            fields=[
                ('user_folder_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='for uploading', max_length=20)),
                ('time_upload', models.DateTimeField(blank=True, null=True)),
                ('time_paid', models.DateTimeField(blank=True, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('folder_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printhub_app.shopfolder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printhub_app.user')),
            ],
            options={
                'db_table': 'user_folder',
            },
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('user_file_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=printhub_app.models.UploadToUserFolder())),
                ('paper_color', models.CharField(max_length=10, null=True)),
                ('page_number', models.CharField(max_length=10, null=True)),
                ('custom_page_size', models.CharField(max_length=10, null=True)),
                ('file_type', models.CharField(max_length=10, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('actual_page_size', models.CharField(blank=True, max_length=10, null=True)),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('file_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printhub_app.userfolder')),
            ],
            options={
                'db_table': 'user_file',
            },
        ),
        migrations.CreateModel(
            name='ShopRate',
            fields=[
                ('shop_rate_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('long_colored_low', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('short_colored_low', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('a4_colored_low', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('long_colored_medium', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('short_colored_medium', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('a4_colored_medium', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('long_colored_high', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('short_colored_high', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('a4_colored_high', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('long_bw', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('short_bw', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('a4_bw', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printhub_app.shop')),
            ],
            options={
                'db_table': 'shop_rate',
            },
        ),
        migrations.CreateModel(
            name='FolderAccessUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printhub_app.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printhub_app.user')),
            ],
            options={
                'db_table': 'folder_access_user',
            },
        ),
    ]
