# Generated by Django 2.0.6 on 2018-10-01 08:25

from django.db import migrations
import invoicing.fields


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0019_recalculate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='customer_vat_id',
            field=invoicing.fields.VATField(blank=True, max_length=14),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='supplier_vat_id',
            field=invoicing.fields.VATField(blank=True, max_length=14),
        ),
    ]
