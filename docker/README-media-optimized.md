

# Synapse Media Optimization Docker Setup

This directory contains Docker configuration for running Synapse with enhanced media optimization features.

## Features

- **Media Compression**: Automatically compresses JPEG and PNG images to reduce storage usage
- **Media Deduplication**: Avoids storing duplicate files by checking content hashes
- **Thumbnail Generation**: Generates thumbnails for images
- **EXIF Extraction**: Extracts metadata from images

## Files

- `Dockerfile-media-optimized`: Dockerfile with media optimization dependencies
- `docker-compose-media-optimized.yml`: Docker Compose configuration
- `homeserver-media-optimized.yaml`: Sample configuration with media optimization enabled

## Setup Instructions

1. **Build the Docker image**:
   ```bash
   cd synapse/docker
   docker-compose -f docker-compose-media-optimized.yml build
   ```

2. **Create data directories**:
   ```bash
   mkdir -p data
   ```

3. **Start the services**:
   ```bash
   docker-compose -f docker-compose-media-optimized.yml up -d
   ```

4. **Access Synapse**:
   - The server will be available at `http://localhost:8008`

## Configuration

The `homeserver-media-optimized.yaml` file contains the following media optimization settings:

```yaml
media:
  # Enable media compression (reduces file size for images)
  enable_media_compression: true

  # Enable media deduplication (avoids storing duplicate files)
  enable_media_deduplication: true

  # Enable thumbnail generation
  enable_thumbnail_generation: true

  # Image compression quality (1-100, higher is better quality but larger file)
  image_compression_quality: 85
```

## Customization

You can adjust the media optimization settings by editing the `homeserver-media-optimized.yaml` file:

- `enable_media_compression`: Set to `false` to disable image compression
- `enable_media_deduplication`: Set to `false` to disable duplicate file detection
- `image_compression_quality`: Adjust between 1-100 to balance quality and file size

## Database Options

By default, this setup uses SQLite. For production use, consider uncommenting the PostgreSQL section in the docker-compose file and updating the configuration accordingly.

## Monitoring

Check the logs to see media optimization in action:

```bash
docker-compose -f docker-compose-media-optimized.yml logs -f synapse
```

You should see log messages about media compression, deduplication, and thumbnail generation.

