# Generated by Django 3.1.14 on 2022-08-23 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0012_auto_20220823_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='evolves_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='descendants', to='pokemon_entities.pokemon', verbose_name='эволюционирует из'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='pokemon_entities.pokemon', verbose_name='покемон'),
        ),
    ]