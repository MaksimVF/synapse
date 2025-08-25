



import hashlib
from PIL import Image
import io

def get_media_hash(data):
    """Generate a hash for media deduplication."""
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def compress_image(data, content_type, max_size=(1920, 1080), quality=85):
    """Compress an image to reduce file size."""
    try:
        if content_type == 'image/jpeg':
            format_name = 'JPEG'
        elif content_type == 'image/png':
            format_name = 'PNG'
        else:
            return data  # Don't compress non-image content

        # Open the image
        image = Image.open(io.BytesIO(data))

        # Convert to RGB if needed (for JPEG)
        if format_name == 'JPEG' and image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize if larger than max_size
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save with compression
        output = io.BytesIO()
        image.save(output, format=format_name, quality=quality, optimize=True)
        return output.getvalue()

    except Exception:
        return data  # Return original if compression fails

# Test the functions
if __name__ == "__main__":
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    test_data = buffer.getvalue()

    # Test hash function
    hash1 = get_media_hash(test_data)
    print(f"Media hash: {hash1}")

    # Test compression
    compressed = compress_image(test_data, 'image/jpeg')
    print(f"Original size: {len(test_data)} bytes")
    print(f"Compressed size: {len(compressed)} bytes")

    # Test hash consistency
    hash2 = get_media_hash(compressed)
    print(f"Compressed hash: {hash2}")
    print(f"Hashes match: {hash1 == hash2}")

    print("Media processing test completed successfully!")



