# Generated by Django 2.0.5 on 2018-06-09 12:37

import display.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appendix',
            fields=[
                ('app_id', models.AutoField(primary_key=True, serialize=False)),
                ('app_type', models.CharField(max_length=10)),
                ('upload_time', models.DateTimeField(verbose_name='uploaded time')),
                ('upload_path', models.FileField(upload_to=display.models.composition_directory_path)),
                ('upload_size', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('comp_id', models.AutoField(primary_key=True, serialize=False)),
                ('comp_name', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(verbose_name='composition uploaded time')),
                ('price', models.DecimalField(decimal_places=1, default=0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='ExpertDetail',
            fields=[
                ('custompk', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('intro', models.CharField(max_length=512)),
                ('account', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Expertuser_relation')),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst_name', models.CharField(max_length=30)),
                ('inst_en_name', models.CharField(max_length=45)),
                ('inst_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=50)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.ExpertDetail')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('composition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='display.Composition')),
                ('origin', models.CharField(max_length=25)),
                ('abstract', models.CharField(max_length=200)),
                ('keyword', models.CharField(max_length=40)),
            ],
            bases=('display.composition',),
        ),
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('composition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='display.Composition')),
                ('patent_type', models.CharField(max_length=25)),
                ('patent_no', models.CharField(max_length=25)),
                ('apply_time', models.DateTimeField(verbose_name='patent applied time')),
                ('auth_time', models.DateTimeField(verbose_name='patent authorized time')),
            ],
            bases=('display.composition',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('composition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='display.Composition')),
                ('proj_type', models.CharField(max_length=25)),
                ('organization', models.CharField(max_length=25)),
                ('expense', models.IntegerField()),
                ('start_time', models.DateTimeField(verbose_name='project started time')),
                ('end_time', models.DateTimeField(verbose_name='project ended time')),
            ],
            bases=('display.composition',),
        ),
        migrations.AddField(
            model_name='institute',
            name='members',
            field=models.ManyToManyField(through='display.Membership', to='display.ExpertDetail'),
        ),
        migrations.AddField(
            model_name='composition',
            name='expert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Expertuser_relation'),
        ),
        migrations.AddField(
            model_name='appendix',
            name='composition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Composition'),
        ),
    ]
