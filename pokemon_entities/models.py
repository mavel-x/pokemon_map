from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    japanese_name = models.CharField(max_length=200, null=True, blank=True)
    english_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    evolves_from = models.ForeignKey('self', null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='ancestors')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField()
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title} at {self.latitude}, {self.longitude}'
