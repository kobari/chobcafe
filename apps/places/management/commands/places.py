from django.core.management.base import BaseCommand, CommandError
from places.places import Places


class Command(BaseCommand):
    help = 'Google Places API '

    def add_arguments(self, parser):
        parser.add_argument('--update_places', dest='update_places', action='store_true')
        parser.add_argument('--write_json', action='store_true')
        parser.add_argument('--text_search', action='store_true')
        parser.add_argument('--place_photos', action='store_true')
        parser.add_argument('--place_detail', action='store_true')
        parser.add_argument('--place_detail_update', action='store_true')
        parser.add_argument('--place_id', nargs='*')

    def handle(self, *args, **options):
        app = Places()
        print(options)
        if options['text_search']:
            app.text_search()
            app.places_update_or_create()
        if options['update_places']:
            app.places_update_or_create()
        if options['place_photos']:
            app.place_photos()
        if options['write_json']:
            print(app.write_json())
        if options['place_detail']:
            app.place_detail(options['place_id'])
            app.place_details_update_or_create()
        if options['place_detail_update']:
            app.places_update_or_create()
