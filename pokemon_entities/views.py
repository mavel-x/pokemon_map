import folium

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in PokemonEntity.objects.filter(
            Q(appeared_at__lte=timezone.localtime()),
            Q(disappeared_at__gt=timezone.localtime()) | Q(disappeared_at__isnull=True)
    ):
        add_pokemon(
            folium_map, entity.latitude,
            entity.longitude,
            request.build_absolute_uri(entity.pokemon.image.url) if entity.pokemon.image
            else DEFAULT_IMAGE_URL,
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image
            else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon.entities.filter(
            Q(appeared_at__lte=timezone.localtime()),
            Q(disappeared_at__gt=timezone.localtime()) | Q(disappeared_at__isnull=True)
    ):
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(requested_pokemon.image.url) if requested_pokemon.image
            else DEFAULT_IMAGE_URL,
        )

    pokemon = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.english_name,
        "title_jp": requested_pokemon.japanese_name,
        "description": requested_pokemon.description,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url) if requested_pokemon.image
        else DEFAULT_IMAGE_URL,
    }
    if requested_pokemon.evolves_from:
        previous_evolution = requested_pokemon.evolves_from
        pokemon.update({
            "previous_evolution": {
                "title_ru": previous_evolution.title,
                "pokemon_id": previous_evolution.id,
                "img_url": request.build_absolute_uri(previous_evolution.image.url) if previous_evolution.image
                else DEFAULT_IMAGE_URL
            }
        })
    evolves_to = Pokemon.objects.filter(evolves_from=requested_pokemon)
    if evolves_to:
        next_evolution = evolves_to.first()
        pokemon.update({
            "next_evolution": {
                "title_ru": next_evolution.title,
                "pokemon_id": next_evolution.id,
                "img_url": request.build_absolute_uri(next_evolution.image.url) if next_evolution.image
                else DEFAULT_IMAGE_URL
            }
        })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
