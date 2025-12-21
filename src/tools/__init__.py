"""Agent tools for model selection, recommendations, and media generation."""

from .model_selector import (
    get_available_models,
    get_model_recommendation,
    compare_models
)

from .gemini_image import (
    generate_image,
    edit_image,
)

from .gemini_image_understanding import (
    understand_image,
    detect_objects,
    segment_objects,
)

from .gemini_video import (
    generate_video,
    generate_video_from_image,
    extend_video,
)

from .gemini_video_understanding import (
    understand_video,
)

from .gemini_music import (
    generate_music,
    generate_music_weighted,
)

__all__ = [
    # Model selector tools
    "get_available_models",
    "get_model_recommendation",
    "compare_models",
    # Gemini image tools
    "generate_image",
    "edit_image",
    # Gemini image understanding tools
    "understand_image",
    "detect_objects",
    "segment_objects",
    # Gemini video tools
    "generate_video",
    "generate_video_from_image",
    "extend_video",
    "understand_video",
    # Gemini music tools
    "generate_music",
    "generate_music_weighted",
]

