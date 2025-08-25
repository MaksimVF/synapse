

# This file is licensed under the Affero General Public License (AGPL) version 3.
#
# Copyright 2025 OpenHands
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# See the GNU Affero General Public License for more details:
# <https://www.gnu.org/licenses/agpl-3.0.html>.

"""
Media processing utilities for Synapse.
"""

import io
import logging
from typing import Optional, Tuple

from PIL import Image
from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)

def compress_image(data: bytes, quality: int = 85) -> bytes:
    """
    Compress JPEG/PNG images to reduce file size.

    Args:
        data: Image data as bytes
        quality: JPEG quality (1-100), higher is better quality but larger file

    Returns:
        Compressed image data
    """
    try:
        img = Image.open(io.BytesIO(data))
        output = io.BytesIO()

        if img.format == 'JPEG':
            img.save(output, format='JPEG', quality=quality, optimize=True)
        elif img.format == 'PNG':
            img.save(output, format='PNG', optimize=True)
        else:
            # Return original if not supported
            return data

        return output.getvalue()
    except Exception as e:
        logger.warning("Failed to compress image: %s", e)
        return data

def generate_thumbnail(data: bytes, size: Tuple[int, int] = (320, 240)) -> Optional[bytes]:
    """
    Generate thumbnail for an image.

    Args:
        data: Image data as bytes
        size: Desired thumbnail size (width, height)

    Returns:
        Thumbnail data as bytes, or None if failed
    """
    try:
        img = Image.open(io.BytesIO(data))
        img.thumbnail(size)

        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except Exception as e:
        logger.warning("Failed to generate thumbnail: %s", e)
        return None

def extract_exif(data: bytes) -> dict:
    """
    Extract EXIF metadata from an image.

    Args:
        data: Image data as bytes

    Returns:
        Dictionary of EXIF tags and values
    """
    try:
        img = Image.open(io.BytesIO(data))
        exif_data = {}

        if hasattr(img, '_getexif'):
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value

        return exif_data
    except Exception as e:
        logger.warning("Failed to extract EXIF data: %s", e)
        return {}

def get_media_hash(data: bytes) -> str:
    """
    Generate SHA-256 hash of media content for deduplication.

    Args:
        data: Media data as bytes

    Returns:
        SHA-256 hash as hex string
    """
    import hashlib
    return hashlib.sha256(data).hexdigest()

