from django.db import migrations, models

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    categories = [
        {'name': 'Výstupní zařízení', 'description': 'Kategorie zahrnující výstupní zařízení jako monitory, tiskárny atd.'},
        {'name': 'Vstupní zařízení', 'description': 'Kategorie zahrnující vstupní zařízení jako klávesnice, myši atd.'},
        {'name': 'Digitální produkty', 'description': 'Kategorie zahrnující digitální produkty jako software, e-knihy atd.'},
    ]
    for category_data in categories:
        Category.objects.create(**category_data)

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=models.CASCADE, related_name='products', to='store.Category'),
            preserve_default=False,
        ),
        migrations.RunPython(create_default_categories),
    ]