# /code/api/crud/crud_semester.py

from typing import List, Optional
from sport.models import Semester


def get_ongoing_semester() -> Optional[Semester]:
    """
    Retrieves current ongoing semester.
    Возвращает объект Semester, чей id = текущий семестр (current_semester()),
    или None, если такого нет.
    """
    qs = Semester.objects.raw('SELECT * FROM semester WHERE id = current_semester()')
    try:
        return next(iter(qs))
    except StopIteration:
        return None


def get_semester_crud(current: bool, with_ft_exercises: bool) -> List[Semester]:
    if current:
        ongoing = get_ongoing_semester()
        return [ongoing] if ongoing is not None else []
    elif with_ft_exercises:
        return list(Semester.objects.filter(fitnesstestexercise__isnull=False).distinct())
    else:
        return list(Semester.objects.all())