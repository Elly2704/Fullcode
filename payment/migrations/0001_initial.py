# Generated by Django 5.0.7 on 2024-08-07 10:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False)),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='payment.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Shipping Address',
                'verbose_name_plural': 'Shipping Addresses',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.shippingaddress'),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gt', 0)), name='quantity_gte_0'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created'], name='payment_ord_created_6a6f0c_idx'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(check=models.Q(('amount__gte', 0)), name='amount_gte_0'),
        ),
    ]
