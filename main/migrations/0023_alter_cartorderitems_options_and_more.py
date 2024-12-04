
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_useraddressbook_mobile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': '8. Orders details'},
        ),
        migrations.RenameField(
            model_name='cartorderitems',
            old_name='invoice_no',
            new_name='order_no',
        ),
    ]
