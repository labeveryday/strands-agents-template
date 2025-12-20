"""
Gemini Image Generation Tool

Uses gemini-3-pro-image-preview for high-quality image generation.
Supports various aspect ratios and resolutions (1K, 2K, 4K).
"""

import os
import base64
from pathlib import Path
from datetime import datetime
from strands import tool
from google import genai
from google.genai import types


@tool
def generate_image(
    prompt: str,
    output_dir: str = "output",
) -> dict:
    """
    Generate an image using Gemini 3 Pro Image Preview.

    Args:
        prompt: Text description of the image to generate. Be specific and descriptive.
        output_dir: Directory to save the generated image (default: "output")

    Returns:
        dict with keys:
            - success: bool indicating if generation succeeded
            - file_path: path to saved image (if successful)
            - message: status message
            - error: error message (if failed)

    Notes:
        - Gemini 3 Pro Image Preview generates high quality images
        - Output is PNG format
        - Requires GOOGLE_API_KEY environment variable
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "GOOGLE_API_KEY environment variable not set"
        }

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        # Extract image from response
        image_data = None
        text_response = None

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                elif hasattr(part, 'text') and part.text:
                    text_response = part.text

        if not image_data:
            return {
                "success": False,
                "error": "No image data in response",
                "text_response": text_response
            }

        # Save image
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gemini_image_{timestamp}.png"
        file_path = output_path / filename

        with open(file_path, "wb") as f:
            f.write(image_data)

        return {
            "success": True,
            "file_path": str(file_path),
            "message": f"Image saved to {file_path}",
            "text_response": text_response
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool
def edit_image(
    prompt: str,
    image_path: str,
    output_dir: str = "output",
    mask_path: str = None,
) -> dict:
    """
    Edit an existing image using Gemini 3 Pro Image Preview.

    Args:
        prompt: Text description of the edits to make.
        image_path: Path to the input image to edit.
        output_dir: Directory to save the edited image (default: "output")
        mask_path: Optional path to a mask image for targeted edits.

    Returns:
        dict with keys:
            - success: bool indicating if edit succeeded
            - file_path: path to saved image (if successful)
            - message: status message
            - error: error message (if failed)

    Notes:
        - Supports PNG, JPEG, and WebP input formats
        - Mask should be black (keep) and white (edit) areas
        - Requires GOOGLE_API_KEY environment variable
    """
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

        contents = [
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt
        ]

        # Add mask if provided
        if mask_path:
            mask_file = Path(mask_path)
            if mask_file.exists():
                with open(mask_file, "rb") as f:
                    mask_bytes = f.read()
                mask_suffix = mask_file.suffix.lower()
                mask_mime = mime_map.get(mask_suffix, "image/png")
                contents.insert(1, types.Part.from_bytes(data=mask_bytes, mime_type=mask_mime))

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        # Extract image from response
        image_data = None
        text_response = None

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                elif hasattr(part, 'text') and part.text:
                    text_response = part.text

        if not image_data:
            return {
                "success": False,
                "error": "No image data in response",
                "text_response": text_response
            }

        # Save image
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gemini_edited_{timestamp}.png"
        file_path = output_path / filename

        with open(file_path, "wb") as f:
            f.write(image_data)

        return {
            "success": True,
            "file_path": str(file_path),
            "message": f"Edited image saved to {file_path}",
            "text_response": text_response
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
