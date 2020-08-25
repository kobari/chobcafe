from django.core.management.base import BaseCommand, CommandError
from places.places import Places


class Command(BaseCommand):

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
        if options['text_search']:
            app.text_search()
        if options['update_places']:
            app.places_bulk_insert()
        if options['place_photos']:
            app.place_photos()
        if options['write_json']:
            print(app.write_json())
        if options['place_detail']:
            print(options)
            app.place_detail(options['place_id'])
        if options['place_detail_update']:
            app.place_details_bulk_insert()
