
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='order_status',
            field=models.BooleanField(default=False),
        ),
    ]
