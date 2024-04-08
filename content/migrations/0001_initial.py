# Generated by Django 5.0.4 on 2024-04-07 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('subTitle', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=5000)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
            ],
        ),
    ]
