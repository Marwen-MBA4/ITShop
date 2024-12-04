
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_cartorder_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('process', 'In Process'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='process', max_length=100),
        ),
    ]
