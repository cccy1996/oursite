# Generated by Django 2.0.5 on 2018-06-03 09:33

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
            name='Inbox',
            fields=[
                ('inbox_id', models.AutoField(primary_key=True, serialize=False)),
                ('inbox_date', models.DateTimeField(verbose_name='inbox message date')),
                ('inbox_content', models.CharField(max_length=255)),
                ('inbox_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_receive', to=settings.AUTH_USER_MODEL)),
                ('inbox_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sends', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
