
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_useraddressbook_options_alter_wishlist_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddressbook',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
    ]
