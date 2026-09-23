# Los modelos reales viven en api.models.
# Esta app solo re-exporta esos modelos para no romper imports antiguos.
from api.models import (
    Autor,
    Editorial,
    Lector,
    Libro,
    Libro_Autor,
    Libro_Editorial,
    Prestamo,
)

__all__ = [
    'Autor',
    'Editorial',
    'Lector',
    'Libro',
    'Libro_Autor',
    'Libro_Editorial',
    'Prestamo',
]
