"""Generate storyboards from keyframes"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from jinja2 import Template
from datetime import datetime

from .layout import StoryboardLayout, GridLayout
from ..video_processor.keyframe_selector import Keyframe


class StoryboardGenerator:
    """Generate visual storyboards from keyframes"""

    def __init__(
        self,
        layout: Optional[StoryboardLayout] = None,
        title: str = "Movie Storyboard"
    ):
        """
        Initialize storyboard generator

        Args:
            layout: StoryboardLayout instance
            title: Storyboard title
        """
        self.layout = layout or GridLayout()
        self.title = title

    def generate_image(
        self,
        keyframes: List[Keyframe],
        captions: Optional[List[str]] = None,
        output_path: str = "storyboard.png"
    ) -> str:
        """
        Generate storyboard as a single image

        Args:
            keyframes: List of Keyframe objects
            captions: Optional list of captions for each frame
            output_path: Output file path

        Returns:
            Path to generated storyboard
        """
        if not keyframes:
            raise ValueError("No keyframes provided")

        # Calculate dimensions
        width, height = self.layout.calculate_dimensions(len(keyframes))

        # Create canvas
        storyboard = Image.new('RGB', (width, height), self.layout.background_color)
        draw = ImageDraw.Draw(storyboard)

        # Try to load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                                           self.layout.font_size_title)
            caption_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                                             self.layout.font_size_caption)
            meta_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                                          self.layout.font_size_metadata)
        except:
            title_font = ImageFont.load_default()
            caption_font = ImageFont.load_default()
            meta_font = ImageFont.load_default()

        # Draw title
        title_bbox = draw.textbbox((0, 0), self.title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        draw.text((title_x, self.layout.padding), self.title,
                 fill=self.layout.text_color, font=title_font)

        # Draw frames
        for idx, keyframe in enumerate(keyframes):
            x, y = self.layout.get_frame_position(idx)

            # Resize and paste frame
            frame_img = Image.fromarray(keyframe.frame.image)
            frame_img = frame_img.resize(
                (self.layout.image_width, self.layout.image_height),
                Image.Resampling.LANCZOS
            )

            # Draw border
            draw.rectangle(
                [x - self.layout.border_width,
                 y - self.layout.border_width,
                 x + self.layout.image_width + self.layout.border_width,
                 y + self.layout.image_height + self.layout.border_width],
                outline=self.layout.border_color,
                width=self.layout.border_width
            )

            storyboard.paste(frame_img, (x, y))

            # Draw caption
            caption_y = y + self.layout.image_height + 5

            # Time stamp
            time_str = f"{int(keyframe.frame.timestamp // 60):02d}:{int(keyframe.frame.timestamp % 60):02d}"
            scene_str = f"Scene {keyframe.scene_number}"
            meta_text = f"{scene_str} - {time_str}"
            draw.text((x, caption_y), meta_text,
                     fill=self.layout.text_color, font=meta_font)

            # Custom caption if provided
            if captions and idx < len(captions):
                caption_text_y = caption_y + 15
                # Wrap text if too long
                caption = captions[idx]
                if len(caption) > 50:
                    caption = caption[:47] + "..."
                draw.text((x, caption_text_y), caption,
                         fill=self.layout.text_color, font=caption_font)

        # Save storyboard
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        storyboard.save(str(output_path), quality=95)

        return str(output_path)

    def generate_pdf(
        self,
        keyframes: List[Keyframe],
        captions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        output_path: str = "storyboard.pdf"
    ) -> str:
        """
        Generate storyboard as PDF

        Args:
            keyframes: List of Keyframe objects
            captions: Optional list of captions
            metadata: Optional metadata dict (title, duration, etc.)
            output_path: Output file path

        Returns:
            Path to generated PDF
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        c = canvas.Canvas(str(output_path), pagesize=letter)
        page_width, page_height = letter

        # Title page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width / 2, page_height - 100, self.title)

        if metadata:
            c.setFont("Helvetica", 12)
            y = page_height - 150
            for key, value in metadata.items():
                c.drawString(100, y, f"{key}: {value}")
                y -= 20

        c.setFont("Helvetica", 10)
        c.drawCentredString(page_width / 2, 50,
                           f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        c.showPage()

        # Storyboard pages
        frames_per_page = self.layout.columns * 2  # 2 rows per page
        margin = 50
        available_width = page_width - 2 * margin
        available_height = page_height - 2 * margin

        frame_width = (available_width - (self.layout.columns - 1) * 20) / self.layout.columns
        frame_height = frame_width * 9 / 16  # 16:9 aspect ratio

        for page_start in range(0, len(keyframes), frames_per_page):
            page_frames = keyframes[page_start:page_start + frames_per_page]

            for idx, keyframe in enumerate(page_frames):
                row = idx // self.layout.columns
                col = idx % self.layout.columns

                x = margin + col * (frame_width + 20)
                y = page_height - margin - (row + 1) * (frame_height + 60)

                # Draw frame
                frame_img = Image.fromarray(keyframe.frame.image)
                img_reader = ImageReader(frame_img)
                c.drawImage(img_reader, x, y, width=frame_width, height=frame_height)

                # Draw caption
                c.setFont("Helvetica-Bold", 10)
                time_str = f"{int(keyframe.frame.timestamp // 60):02d}:{int(keyframe.frame.timestamp % 60):02d}"
                caption_text = f"Scene {keyframe.scene_number} - {time_str}"
                c.drawString(x, y - 15, caption_text)

                if captions and (page_start + idx) < len(captions):
                    c.setFont("Helvetica", 9)
                    caption = captions[page_start + idx]
                    # Wrap text
                    max_width = frame_width
                    if len(caption) > 60:
                        caption = caption[:57] + "..."
                    c.drawString(x, y - 30, caption)

            c.showPage()

        c.save()
        return str(output_path)

    def generate_html(
        self,
        keyframes: List[Keyframe],
        captions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        output_path: str = "storyboard.html",
        frames_dir: Optional[str] = None
    ) -> str:
        """
        Generate interactive HTML storyboard

        Args:
            keyframes: List of Keyframe objects
            captions: Optional list of captions
            metadata: Optional metadata dict
            output_path: Output file path
            frames_dir: Directory containing frame images

        Returns:
            Path to generated HTML
        """
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .metadata {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .storyboard {
            display: grid;
            grid-template-columns: repeat({{ columns }}, 1fr);
            gap: 20px;
        }
        .frame {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .frame:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .frame img {
            width: 100%;
            height: auto;
            border-radius: 4px;
        }
        .frame-info {
            margin-top: 10px;
        }
        .scene-number {
            font-weight: bold;
            color: #0066cc;
        }
        .timestamp {
            color: #666;
            font-size: 0.9em;
        }
        .caption {
            margin-top: 8px;
            color: #333;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>

    {% if metadata %}
    <div class="metadata">
        {% for key, value in metadata.items() %}
        <p><strong>{{ key }}:</strong> {{ value }}</p>
        {% endfor %}
    </div>
    {% endif %}

    <div class="storyboard">
        {% for frame in frames %}
        <div class="frame">
            <img src="data:image/png;base64,{{ frame.image_data }}" alt="Scene {{ frame.scene_number }}">
            <div class="frame-info">
                <div>
                    <span class="scene-number">Scene {{ frame.scene_number }}</span>
                    <span class="timestamp">{{ frame.timestamp }}</span>
                </div>
                {% if frame.caption %}
                <div class="caption">{{ frame.caption }}</div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
        """

        # Prepare frame data
        import base64
        import io

        frames_data = []
        for idx, keyframe in enumerate(keyframes):
            # Convert frame to base64
            img = Image.fromarray(keyframe.frame.image)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()

            time_str = f"{int(keyframe.frame.timestamp // 60):02d}:{int(keyframe.frame.timestamp % 60):02d}"

            frames_data.append({
                "image_data": img_str,
                "scene_number": keyframe.scene_number,
                "timestamp": time_str,
                "caption": captions[idx] if captions and idx < len(captions) else ""
            })

        # Render template
        template = Template(html_template)
        html_content = template.render(
            title=self.title,
            metadata=metadata,
            columns=self.layout.columns,
            frames=frames_data
        )

        # Save HTML
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')

        return str(output_path)
