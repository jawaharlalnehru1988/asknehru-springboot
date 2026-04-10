import mimetypes
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import connection
from django.http import FileResponse, Http404

from medicines.models import Medicine
from .serializer_utils import file_suffix


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_uploaded_file(uploaded_file, directory: Path) -> str:
    ensure_directory(directory)
    filename = f"{uuid4()}{file_suffix(uploaded_file)}"
    target = directory / filename
    with target.open("wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return filename


def delete_shared_file(filename: str | None) -> None:
    if not filename:
        return
    path = settings.ASKNEHRU_SHARED_UPLOAD_DIR / filename
    if path.exists():
        path.unlink()


def delete_managed_media(media_ref: str | None, directory: Path, public_prefix: str) -> None:
    if not media_ref:
        return
    candidate = media_ref.strip()
    if "/" in candidate:
        if not candidate.startswith(public_prefix) and not candidate.startswith(public_prefix.lstrip("/")):
            return
        candidate = Path(candidate).name
    target = directory / candidate
    if target.exists():
        target.unlink()


def delete_replaced_media(
    existing_media_ref: str | None,
    updated_media_ref: str | None,
    directory: Path,
    public_prefix: str,
) -> None:
    if not existing_media_ref:
        return
    existing_value = existing_media_ref.strip()
    updated_value = (updated_media_ref or "").strip()
    if existing_value == updated_value:
        return
    delete_managed_media(existing_value, directory, public_prefix)


def get_medicine_values(table_name: str, value_column: str, medicine_ids: list[int]) -> dict[int, list[str]]:
    if not medicine_ids:
        return {}

    placeholders = ", ".join(["%s"] * len(medicine_ids))
    query = (
        f"SELECT medicine_id, {value_column} FROM {table_name} "
        f"WHERE medicine_id IN ({placeholders}) ORDER BY medicine_id"
    )
    mapping = {medicine_id: [] for medicine_id in medicine_ids}
    with connection.cursor() as cursor:
        cursor.execute(query, medicine_ids)
        for medicine_id, value in cursor.fetchall():
            mapping.setdefault(medicine_id, []).append(value)
    return mapping


def set_medicine_values(medicine_id: int, table_name: str, value_column: str, values: list[str]) -> None:
    cleaned_values = [value.strip() for value in values if value and value.strip()]
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table_name} WHERE medicine_id = %s", [medicine_id])
        if cleaned_values:
            rows = [(medicine_id, value) for value in cleaned_values]
            cursor.executemany(
                f"INSERT INTO {table_name} (medicine_id, {value_column}) VALUES (%s, %s)",
                rows,
            )


def attach_medicine_collections(medicines: list[Medicine]) -> list[Medicine]:
    medicine_ids = [medicine.id for medicine in medicines]
    ingredients = get_medicine_values("medicine_ingredients", "ingredient", medicine_ids)
    side_effects = get_medicine_values("medicine_side_effects", "side_effect", medicine_ids)
    benefits = get_medicine_values("medicine_benefits", "benefit", medicine_ids)

    for medicine in medicines:
        medicine.ingredients = ingredients.get(medicine.id, [])
        medicine.sideEffects = side_effects.get(medicine.id, [])
        medicine.benefits = benefits.get(medicine.id, [])
    return medicines


def attach_medicine_collections_single(medicine: Medicine) -> Medicine:
    return attach_medicine_collections([medicine])[0]


def build_upload_response(filename: str, prefix: str) -> dict[str, str]:
    return {
        "url": f"{settings.ASKNEHRU_BASE_URL}{prefix}{filename}",
        "filename": filename,
    }


def get_shared_file_response(filename: str):
    path = settings.ASKNEHRU_SHARED_UPLOAD_DIR / filename
    if not path.exists() or not path.is_file():
        raise Http404
    content_type, _ = mimetypes.guess_type(path.name)
    response = FileResponse(path.open("rb"), content_type=content_type or "application/octet-stream")
    response["Content-Disposition"] = f'inline; filename="{path.name}"'
    return response