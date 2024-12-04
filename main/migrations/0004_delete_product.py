from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_brand_image_alter_category_image_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
