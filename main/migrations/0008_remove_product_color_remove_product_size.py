
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_banner_options_alter_brand_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]
