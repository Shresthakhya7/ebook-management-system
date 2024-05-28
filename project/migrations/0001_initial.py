# Generated by Django 4.2.9 on 2024-05-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('file', models.FileField(upload_to='ebooks/')),
            ],
        ),
    ]