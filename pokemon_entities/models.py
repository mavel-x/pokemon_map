from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон."""
    title = models.CharField('название', max_length=200)
    image = models.ImageField('картинка', upload_to='images', null=True, blank=True)
    japanese_name = models.CharField('японское название', max_length=200, null=True, blank=True)
    english_name = models.CharField('английское название', max_length=200, null=True, blank=True)
    description = models.TextField('описание', null=True, blank=True)
    evolves_from = models.ForeignKey('self', null=True, blank=True,
                                     verbose_name='эволюционирует из', on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Особь покемона, появляющаяся в мире."""
    pokemon = models.ForeignKey(Pokemon, verbose_name='покемон', on_delete=models.CASCADE)
    latitude = models.FloatField('широта')
    longitude = models.FloatField('долгота')
    appeared_at = models.DateTimeField('когда появился')
    disappeared_at = models.DateTimeField('когда исчез', null=True, blank=True)
    level = models.IntegerField('уровень', null=True, blank=True)
    health = models.IntegerField('здоровье', null=True, blank=True)
    strength = models.IntegerField('атака', null=True, blank=True)
    defense = models.IntegerField('защита', null=True, blank=True)
    stamina = models.IntegerField('выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title} at {self.latitude}, {self.longitude}'
