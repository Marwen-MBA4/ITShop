
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_cartorderitems_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='order_dt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
