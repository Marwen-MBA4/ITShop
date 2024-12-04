
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_productreview_options_alter_wishlist_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraddressbook',
            options={'verbose_name_plural': 'AddressBook'},
        ),
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name_plural': 'Wishlist'},
        ),
        migrations.AddField(
            model_name='useraddressbook',
            name='mobile',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
