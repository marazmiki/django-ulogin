import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ULoginUser',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('network', models.CharField(
                    choices=[
                        ('vkontakte', 'V Kontakte'),
                        ('odnoklassniki', 'Odnoklassniki'),
                        ('mailru', 'Mail.Ru'),
                        ('yandex', 'Yandex'),
                        ('lastfm', 'Last.FM'),
                        ('linkedin', 'LinkedIn'),
                        ('google', 'Google'),
                        ('soundcloud', 'SoundCloud'),
                        ('steam', 'Steam'),
                        ('liveid', 'Windows Live ID'),
                        ('vimeo', 'Vimeo'),
                        ('openid', 'OpenID'),
                        ('webmoney', 'WebMoney'),
                        ('flickr', 'Flickr'),
                        ('youtube', 'YouTube'),
                        ('livejournal', 'LiveJournal'),
                        ('twitter', 'Twitter'),
                        ('facebook', 'Facebook'),
                        ('foursquare', 'Foursquare'),
                        ('googleplus', 'Google+'),
                        ('tumblr', 'Tumblr'),
                        ('wargaming', 'Wargaming.net'),
                        ('instagram', 'Instagram'),
                        ('uid', 'uID'),
                    ],
                    db_index=True,
                    max_length=255,
                    verbose_name='network')),
                ('identity', models.URLField(
                    db_index=True,
                    max_length=255,
                    verbose_name='identity')),
                ('uid', models.CharField(
                    db_index=True,
                    max_length=255,
                    verbose_name='uid')),
                ('date_created', models.DateTimeField(
                    default=django.utils.timezone.now,
                    editable=False,
                    verbose_name='date created')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ulogin_users',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='user')),
            ],
            options={
                'verbose_name': 'ulogin user',
                'verbose_name_plural': 'ulogin users',
            },
        ),
        migrations.AlterUniqueTogether(
            name='uloginuser',
            unique_together={('network', 'uid')},
        ),
    ]
