# Generated by Django 4.2.3 on 2024-02-10 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("business", "0004_customer_quotation_lineitem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="title",
            new_name="name",
        ),
    ]