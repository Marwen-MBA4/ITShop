
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_product_options_alter_productattribute_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.PositiveIntegerField()),
                ('cart_password', models.CharField(max_length=100)),
            ],
        ),
    ]
