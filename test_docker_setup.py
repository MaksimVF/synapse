




import os
import sys

def test_docker_files():
    """Test that all required Docker files exist."""

    required_files = [
        'docker/Dockerfile',
        'docker/Dockerfile-media-optimized',
        'docker/docker-compose.yml',
        'docker/docker-compose-media-optimized.yml',
        'docker/conf/homeserver.yaml',
        'docker/conf/homeserver-media-optimized.yaml',
        'docker/conf/homeserver.log.config',
        'docker/README.md'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(f'/workspace/synapse/{file_path}'):
            missing_files.append(file_path)

    if missing_files:
        print(f"ERROR: Missing Docker files: {missing_files}")
        return False

    print("All required Docker files are present.")
    return True

def test_media_processing_import():
    """Test that media processing functions can be imported."""

    try:
        sys.path.append('/workspace/synapse')
        from synapse.media.media_processing import (
            get_media_hash,
            compress_image,
            generate_thumbnail,
            extract_exif
        )
        print("Media processing functions imported successfully.")
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import media processing functions: {e}")
        return False

def test_media_processing_functions():
    """Test that media processing functions work correctly."""

    try:
        import io
        from PIL import Image
        from synapse.media.media_processing import get_media_hash, compress_image

        # Create a test image
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        test_data = buffer.getvalue()

        # Test hash function
        hash1 = get_media_hash(test_data)
        hash2 = get_media_hash(test_data)
        assert hash1 == hash2, "Hash consistency test failed"

        # Test compression
        compressed = compress_image(test_data, 'image/jpeg')
        assert len(compressed) < len(test_data), "Compression test failed"

        print("Media processing functions work correctly.")
        return True

    except Exception as e:
        print(f"ERROR: Media processing functions test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Docker setup...")

    success = True
    success &= test_docker_files()
    success &= test_media_processing_import()
    success &= test_media_processing_functions()

    if success:
        print("\n✅ All tests passed! Docker setup is ready.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)




