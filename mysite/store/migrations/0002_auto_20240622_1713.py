from django.db import migrations, models

def add_image_to_product(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    # Přidání pole image do modelu Product
    Product.objects.all().update(image=None)

class Migration(migrations.Migration):

    dependencies = [
        # Případné závislosti migrace
    ]

    operations = [
        # Přidání sloupce image do modelu Product
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),

        # Upravení dat
        migrations.RunPython(add_image_to_product),
    ]