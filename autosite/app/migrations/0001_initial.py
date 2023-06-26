# Generated by Django 4.2 on 2023-06-26 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Make', models.CharField(max_length=50)),
                ('Model', models.CharField(max_length=50)),
                ('Year', models.IntegerField()),
                ('Fuel', models.CharField(max_length=50)),
                ('Engine_cc', models.IntegerField()),
                ('Gearbox', models.CharField(max_length=50)),
                ('Color', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.IntegerField()),
                ('Mileage', models.IntegerField()),
                ('Location', models.CharField(max_length=50)),
                ('Description', models.TextField()),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Phone', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=50)),
                ('Car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.car')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='listing_images/')),
                ('Listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.listing')),
            ],
        ),
    ]
