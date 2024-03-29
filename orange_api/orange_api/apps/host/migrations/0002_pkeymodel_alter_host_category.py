# Generated by Django 4.1.7 on 2023-04-25 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PkeyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='描述信息')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('private', models.TextField(verbose_name='私钥')),
                ('public', models.TextField(verbose_name='公钥')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='host',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='hostcategory', to='host.hostcategory', verbose_name='主机类别'),
        ),
    ]
