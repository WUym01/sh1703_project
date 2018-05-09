# Generated by Django 2.0.5 on 2018-05-09 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(verbose_name='余额')),
                ('balance_available', models.IntegerField(verbose_name='可用余额')),
                ('balance_freeze', models.IntegerField(verbose_name='冻结金额')),
            ],
        ),
        migrations.CreateModel(
            name='CardHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('remark', models.TextField(verbose_name='说明')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cards.Card', verbose_name='银行卡')),
            ],
        ),
        migrations.CreateModel(
            name='CardInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('phone', models.CharField(max_length=64, verbose_name='电话')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('card', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cards.Card')),
            ],
        ),
        migrations.CreateModel(
            name='CardOperate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='名称')),
                ('remark', models.TextField(verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='CardStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='名称')),
                ('remark', models.TextField(blank=True, verbose_name='备注')),
            ],
        ),
        migrations.AddField(
            model_name='cardhistory',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cards.CardOperate', verbose_name='操作类型'),
        ),
        migrations.AddField(
            model_name='card',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.CardStatus', verbose_name='状态'),
        ),
    ]
