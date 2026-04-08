import os
import uuid
import urllib.request
from urllib.parse import quote
from typing import Optional

from dotenv import load_dotenv

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
POST_IMAGES_BUCKET = "post-images"


def _build_public_url(object_path: str) -> str:
    return f"{SUPABASE_URL}/storage/v1/object/public/{POST_IMAGES_BUCKET}/{object_path}"


def upload_post_image(file_bytes: bytes, filename: str, content_type: Optional[str] = None) -> str:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("SUPABASE_URL 또는 SUPABASE_SERVICE_ROLE_KEY가 설정되지 않았습니다")

    ext = os.path.splitext(filename)[1] or ".bin"
    object_path = f"{uuid.uuid4().hex}{ext}"
    encoded_path = quote(object_path, safe="")
    upload_url = f"{SUPABASE_URL}/storage/v1/object/{POST_IMAGES_BUCKET}/{encoded_path}"

    req = urllib.request.Request(
        upload_url,
        data=file_bytes,
        method="POST",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": content_type or "application/octet-stream",
            "x-upsert": "false",
        },
    )
    try:
        urllib.request.urlopen(req)
    except Exception as exc:
        raise ValueError("이미지 업로드에 실패했습니다") from exc

    return _build_public_url(object_path)


def delete_post_image(image_url: str):
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("SUPABASE_URL 또는 SUPABASE_SERVICE_ROLE_KEY가 설정되지 않았습니다")

    marker = f"/storage/v1/object/public/{POST_IMAGES_BUCKET}/"
    if marker not in image_url:
        raise ValueError("잘못된 이미지 URL입니다")

    object_path = image_url.split(marker, 1)[1]
    encoded_path = quote(object_path, safe="")
    delete_url = f"{SUPABASE_URL}/storage/v1/object/{POST_IMAGES_BUCKET}/{encoded_path}"

    req = urllib.request.Request(
        delete_url,
        method="DELETE",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        },
    )
    try:
        urllib.request.urlopen(req)
    except Exception as exc:
        raise ValueError("이미지 삭제에 실패했습니다") from exc
