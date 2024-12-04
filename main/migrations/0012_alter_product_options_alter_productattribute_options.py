from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_productattribute_size_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': '5. Products'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'verbose_name_plural': '6. ProductAttributes'},
        ),
    ]
