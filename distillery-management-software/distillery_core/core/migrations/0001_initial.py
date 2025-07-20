from django.db import migrations, models
import django.contrib.auth.models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('batch_type', models.CharField(max_length=100)),
                ('ingredients', models.JSONField()),
                ('process_steps', models.TextField()),
                ('abv_target', models.FloatField(default=0.0)),
                ('fermentation_temp', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='In Progress', max_length=50)),
                ('recipe', models.ForeignKey(on_delete=models.CASCADE, to='core.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Vessel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('capacity', models.FloatField()),
                ('occupied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('item', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('quantity', models.FloatField()),
                ('barcode', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=models.CASCADE, to='core.inventory')),
                ('supplier', models.ForeignKey(on_delete=models.CASCADE, to='core.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('hours', models.FloatField()),
                ('task', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to='auth.user')),
            ],
        ),
        migrations.RunPython(
            code=lambda apps, schema_editor: (
                apps.get_model('core', 'Recipe').objects.bulk_create([
                    apps.get_model('core', 'Recipe')(
                        name='Gin', batch_type='Infusion + Single distillation',
                        ingredients=[
                            {'item': 'Juniper', 'grams_per_liter': 15},
                            {'item': 'Coriander', 'grams_per_liter': 5},
                            {'item': 'Orris Root', 'grams_per_liter': 0.15},
                            {'item': 'Lemon Peel', 'grams_per_liter': 0.5},
                            {'item': 'Timut Peppercorns', 'grams_per_liter': 0.1},
                            {'item': 'Licorice Root', 'grams_per_liter': 0.1},
                            {'item': 'Star Anise', 'grams_per_liter': 0.05}
                        ],
                        process_steps='Place all botanicals in mesh bags, hang in still. Fill with 100L 40% ABV GNS, soak overnight, distill per SOP.',
                        abv_target=40.0
                    ),
                    apps.get_model('core', 'Recipe')(
                        name='Bourbon', batch_type='Fermentation + 1.5 distillation',
                        ingredients=[
                            {'item': 'Corn', 'percent': 75, 'lbs_per_gallon': 2.25},
                            {'item': 'Rye', 'percent': 15, 'lbs_per_gallon': 0.45},
                            {'item': '6-row Barley', 'percent': 10, 'lbs_per_gallon': 0.3}
                        ],
                        process_steps='Mash and ferment grains per SOP, distill 1.5 times in stills.',
                        abv_target=40.0
                    ),
                    apps.get_model('core', 'Recipe')(
                        name='Rye Whisky', batch_type='Fermentation + 1.5 distillation',
                        ingredients=[{'item': 'Rye', 'percent': 100, 'lbs_per_gallon': 3}],
                        process_steps='Mash and ferment rye per SOP, distill 1.5 times in stills.',
                        abv_target=40.0
                    ),
                    apps.get_model('core', 'Recipe')(
                        name='Single Malt Whisky', batch_type='Fermentation + 1.5 distillation',
                        ingredients=[{'item': '2-row Barley', 'percent': 100, 'lbs_per_gallon': 3}],
                        process_steps='Mash and ferment barley per SOP, distill 1.5 times in stills.',
                        abv_target=40.0
                    ),
                    apps.get_model('core', 'Recipe')(
                        name='Vodka', batch_type='Fermentation + Double distillation',
                        ingredients=[{'item': 'Rice Syrup Solids', 'percent': 100, 'lbs_per_gallon': 2}],
                        process_steps='Ferment rice syrup solids per SOP, double distill in stills.',
                        abv_target=40.0
                    ),
                ]),
                apps.get_model('core', 'Vessel').objects.bulk_create([
                    apps.get_model('core', 'Vessel')(name='Fermenter1', type='Conical Fermenter', capacity=465.0),
                    apps.get_model('core', 'Vessel')(name='Fermenter2', type='Conical Fermenter', capacity=465.0),
                    apps.get_model('core', 'Vessel')(name='Still1', type='Pot Still', capacity=100.0),
                    apps.get_model('core', 'Vessel')(name='Still2', type='Pot Still', capacity=100.0),
                    apps.get_model('core', 'Vessel')(name='Storage1', type='Storage Tank', capacity=500.0),
                ]),
                apps.get_model('core', 'Inventory').objects.bulk_create([
                    apps.get_model('core', 'Inventory')(item='Juniper', unit='grams', quantity=15000, barcode='PLACEHOLDER_UPC_1'),
                    apps.get_model('core', 'Inventory')(item='Coriander', unit='grams', quantity=5000, barcode='PLACEHOLDER_UPC_2'),
                    apps.get_model('core', 'Inventory')(item='Orris Root', unit='grams', quantity=150, barcode='PLACEHOLDER_UPC_3'),
                    apps.get_model('core', 'Inventory')(item='Corn', unit='lbs', quantity=300, barcode='PLACEHOLDER_UPC_4'),
                    apps.get_model('core', 'Inventory')(item='Rye', unit='lbs', quantity=100, barcode='PLACEHOLDER_UPC_5'),
                    apps.get_model('core', 'Inventory')(item='6-row Barley', unit='lbs', quantity=50, barcode='PLACEHOLDER_UPC_6'),
                    apps.get_model('core', 'Inventory')(item='2-row Barley', unit='lbs', quantity=50, barcode='PLACEHOLDER_UPC_7'),
                    apps.get_model('core', 'Inventory')(item='Rice Syrup Solids', unit='lbs', quantity=200, barcode='PLACEHOLDER_UPC_8'),
                    apps.get_model('core', 'Inventory')(item='GNS', unit='liters', quantity=1000, barcode='PLACEHOLDER_UPC_9'),
                    apps.get_model('core', 'Inventory')(item='Bottles', unit='units', quantity=500, barcode='PLACEHOLDER_UPC_10'),
                ]),
                apps.get_model('core', 'Supplier').objects.bulk_create([
                    apps.get_model('core', 'Supplier')(name='Brewer Supply Group', contact_email='distilling@rahrbsg.com', contact_phone='1-855-819-3950'),
                    apps.get_model('core', 'Supplier')(name='Placeholder Supplier 1', contact_email='placeholder1@sup.com', contact_phone='555-0001'),
                    apps.get_model('core', 'Supplier')(name='Placeholder Supplier 2', contact_email='placeholder2@sup.com', contact_phone='555-0002'),
                    apps.get_model('core', 'Supplier')(name='Placeholder Supplier 3', contact_email='placeholder3@sup.com', contact_phone='555-0003'),
                    apps.get_model('core', 'Supplier')(name='Placeholder Supplier 4', contact_email='placeholder4@sup.com', contact_phone='555-0004'),
                ]),
                apps.get_model('core', 'Customer').objects.bulk_create([
                    apps.get_model('core', 'Customer')(name='Placeholder Customer 1', contact_email='cust1@place.com', contact_phone='555-1001'),
                    apps.get_model('core', 'Customer')(name='Placeholder Customer 2', contact_email='cust2@place.com', contact_phone='555-1002'),
                    apps.get_model('core', 'Customer')(name='Placeholder Customer 3', contact_email='cust3@place.com', contact_phone='555-1003'),
                ]),
            )
        ),
    ]