"""
Gemini Video Generation Tool

Uses Veo 3.1 for high-quality video generation.
Supports text-to-video and image-to-video generation.
"""

import os
import time
from pathlib import Path
from datetime import datetime
from strands import tool
from google import genai
from google.genai import types


@tool
def generate_video(
    prompt: str,
    output_dir: str = "output",
    duration_seconds: int = 6,
    max_wait_seconds: int = 300,
) -> dict:
    """
    Generate a video using Veo 3.1 (text-to-video).

    Args:
        prompt: Text description of the video to generate. Be specific about motion,
                camera angles, lighting, and style.
        output_dir: Directory to save the generated video (default: "output")
        duration_seconds: Video duration in seconds. Options: 4 or 6 (default: 6)
        max_wait_seconds: Maximum time to wait for generation (default: 300)

    Returns:
        dict with keys:
            - success: bool indicating if generation succeeded
            - file_path: path to saved video (if successful)
            - message: status message
            - error: error message (if failed)

    Notes:
        - Veo 3.1 generates high-quality videos with natural motion
        - Generation is async and may take 1-5 minutes
        - Output is MP4 format
        - Requires GOOGLE_API_KEY environment variable
    """
    valid_durations = [4, 6]
    if duration_seconds not in valid_durations:
        return {
            "success": False,
            "error": f"Invalid duration_seconds. Must be one of: {valid_durations}"
        }

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "GOOGLE_API_KEY environment variable not set"
        }

    try:
        client = genai.Client(api_key=api_key)

        # Build generation config with camelCase parameters
        config = types.GenerateVideosConfig(
            durationSeconds=duration_seconds,
        )

        # Start async video generation
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=config,
        )

        # Poll for completion
        start_time = time.time()
        while not operation.done:
            if time.time() - start_time > max_wait_seconds:
                return {
                    "success": False,
                    "error": f"Video generation timed out after {max_wait_seconds} seconds"
                }
            time.sleep(10)
            operation = client.operations.get(operation)

        # Check for errors
        if operation.error:
            return {
                "success": False,
                "error": f"Generation failed: {operation.error}"
            }

        # Get generated video
        if not operation.response or not operation.response.generated_videos:
            return {
                "success": False,
                "error": "No video generated"
            }

        generated_video = operation.response.generated_videos[0]

        # Save video
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gemini_video_{timestamp}.mp4"
        file_path = output_path / filename

        # Get video data - structure is GeneratedVideo.video.uri or GeneratedVideo.video.video_bytes
        video_obj = generated_video.video if hasattr(generated_video, 'video') else None

        if video_obj and hasattr(video_obj, 'video_bytes') and video_obj.video_bytes:
            with open(file_path, "wb") as f:
                f.write(video_obj.video_bytes)
        elif video_obj and hasattr(video_obj, 'uri') and video_obj.uri:
            # Download with API key authentication
            import requests
            url = video_obj.uri + f"&key={api_key}"
            response = requests.get(url)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to download video: HTTP {response.status_code}"
                }
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            return {
                "success": False,
                "error": "No video data or URI in response"
            }

        return {
            "success": True,
            "file_path": str(file_path),
            "message": f"Video saved to {file_path}",
            "duration": duration_seconds,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool
def generate_video_from_image(
    prompt: str,
    image_path: str,
    output_dir: str = "output",
    duration_seconds: int = 6,
    max_wait_seconds: int = 300,
) -> dict:
    """
    Generate a video from an image using Veo 3.1 (image-to-video).

    Args:
        prompt: Text description of the video motion and animation.
        image_path: Path to the input image (first frame).
        output_dir: Directory to save the generated video (default: "output")
        duration_seconds: Video duration in seconds. Options: 4 or 6 (default: 6)
        max_wait_seconds: Maximum time to wait for generation (default: 300)

    Returns:
        dict with keys:
            - success: bool indicating if generation succeeded
            - file_path: path to saved video (if successful)
            - message: status message
            - error: error message (if failed)

    Notes:
        - The input image becomes the first frame of the video
        - Describe desired motion and camera movement in the prompt
        - Requires GOOGLE_API_KEY environment variable
    """
    valid_durations = [4, 6]
    if duration_seconds not in valid_durations:
        return {
            "success": False,
            "error": f"Invalid duration_seconds. Must be one of: {valid_durations}"
        }

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "GOOGLE_API_KEY environment variable not set"
        }

    image_file = Path(image_path)
    if not image_file.exists():
        return {
            "success": False,
            "error": f"Image file not found: {image_path}"
        }

    try:
        client = genai.Client(api_key=api_key)

        # Read and encode input image
        with open(image_file, "rb") as f:
            image_bytes = f.read()

        # Determine mime type
        suffix = image_file.suffix.lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        mime_type = mime_map.get(suffix, "image/png")

        # Create image object
        image = types.Image(image_bytes=image_bytes, mime_type=mime_type)

        # Build generation config
        config = types.GenerateVideosConfig(
            durationSeconds=duration_seconds,
        )

        # Start async video generation with image
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            image=image,
            config=config,
        )

        # Poll for completion
        start_time = time.time()
        while not operation.done:
            if time.time() - start_time > max_wait_seconds:
                return {
                    "success": False,
                    "error": f"Video generation timed out after {max_wait_seconds} seconds"
                }
            time.sleep(10)
            operation = client.operations.get(operation)

        # Check for errors
        if operation.error:
            return {
                "success": False,
                "error": f"Generation failed: {operation.error}"
            }

        # Get generated video
        if not operation.response or not operation.response.generated_videos:
            return {
                "success": False,
                "error": "No video generated"
            }

        generated_video = operation.response.generated_videos[0]

        # Save video
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gemini_video_i2v_{timestamp}.mp4"
        file_path = output_path / filename

        # Get video data - structure is GeneratedVideo.video.uri or GeneratedVideo.video.video_bytes
        video_obj = generated_video.video if hasattr(generated_video, 'video') else None

        if video_obj and hasattr(video_obj, 'video_bytes') and video_obj.video_bytes:
            with open(file_path, "wb") as f:
                f.write(video_obj.video_bytes)
        elif video_obj and hasattr(video_obj, 'uri') and video_obj.uri:
            # Download with API key authentication
            import requests
            url = video_obj.uri + f"&key={api_key}"
            response = requests.get(url)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to download video: HTTP {response.status_code}"
                }
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            return {
                "success": False,
                "error": "No video data or URI in response"
            }

        return {
            "success": True,
            "file_path": str(file_path),
            "message": f"Video saved to {file_path}",
            "source_image": image_path,
            "duration": duration_seconds,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
