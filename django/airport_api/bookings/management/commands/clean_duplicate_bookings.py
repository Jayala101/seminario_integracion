from django.core.management.base import BaseCommand
from django.db.models import Count
from bookings.models import Booking


class Command(BaseCommand):
    help = 'Elimina reservas duplicadas, dejando solo la más reciente por pasajero/vuelo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué se haría sin ejecutar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Encontrar combinaciones duplicadas de pasajero + vuelo
        duplicates = (
            Booking.objects
            .values('passenger', 'flight')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        
        total_duplicates = 0
        total_deleted = 0
        
        self.stdout.write(self.style.WARNING(
            f'Encontradas {len(duplicates)} combinaciones duplicadas de pasajero/vuelo'
        ))
        
        for dup in duplicates:
            # Obtener todas las reservas de esta combinación
            bookings = Booking.objects.filter(
                passenger_id=dup['passenger'],
                flight_id=dup['flight']
            ).order_by('-created_at')  # Más reciente primero
            
            # Mantener solo la primera (más reciente)
            keep = bookings.first()
            to_delete = bookings.exclude(pk=keep.pk)
            
            count = to_delete.count()
            total_duplicates += count
            
            if dry_run:
                self.stdout.write(
                    f'  [DRY RUN] Mantener: {keep.booking_code}, '
                    f'Eliminar {count} duplicados'
                )
                for booking in to_delete:
                    self.stdout.write(f'    - {booking.booking_code}')
            else:
                deleted_count = to_delete.delete()[0]
                total_deleted += deleted_count
                self.stdout.write(self.style.SUCCESS(
                    f'  Mantenida: {keep.booking_code}, '
                    f'Eliminadas {deleted_count} duplicadas'
                ))
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'\n[DRY RUN] Se eliminarían {total_duplicates} reservas duplicadas'
            ))
            self.stdout.write(self.style.WARNING(
                'Ejecuta sin --dry-run para aplicar los cambios'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Eliminadas {total_deleted} reservas duplicadas exitosamente'
            ))
