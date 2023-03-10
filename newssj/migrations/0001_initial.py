# Generated by Django 4.1.6 on 2023-02-04 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(default=0, verbose_name='Author rating')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Category name')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_type', models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], max_length=2)),
                ('post_title', models.CharField(max_length=256, verbose_name='Post name')),
                ('time_in', models.DateTimeField(auto_now_add=True, verbose_name='Post date')),
                ('post_text', models.TextField(verbose_name='Post text')),
                ('rating', models.SmallIntegerField(default=0, verbose_name='Post rating')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newssj.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newssj.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newssj.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='newssj.PostCategory', to='newssj.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=512, verbose_name='Comment text')),
                ('time_in', models.DateTimeField(auto_now_add=True, verbose_name='Post date')),
                ('rating', models.SmallIntegerField(default=0, verbose_name='Comment rating')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newssj.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
