
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_cartorderitems_order_dt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.AddField(
            model_name='product',
            name='identifier',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
