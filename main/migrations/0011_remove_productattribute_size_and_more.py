
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_product_image_productattribute_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='size',
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
