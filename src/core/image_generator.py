import os
import tempfile
import textwrap
from pathlib import Path
import markdown2
from html2image import Html2Image

class ImageGenerator:
    def __init__(self, font_family='Arial', font_size=12, font_path=None, width=400): # Increased default font_size, added width
        self.font_family = font_family
        self.font_size = font_size
        self.font_path = Path(__file__).parent.parent.parent / 'assets' / 'XiaolaiSC-Regular.ttf'
        self.width = width

    def _build_html(self, markdown_text):
        html_body = markdown2.markdown(markdown_text)
        font_abs_path = self.font_path.resolve()
        font_face = ""
        if self.font_path:
            font_face = f"""
            @font-face {{
                font-family: 'CustomFont';
                src: url('file://{font_abs_path}');
            }}
            """
            font_family = 'CustomFont'
        else:
            font_family = self.font_family

        html = f"""
        <html>
        <head>
        <style>
            {font_face}
            body {{
                background-color: #FFFEF8;
                font-family: '{font_family}';
                font-size: {self.font_size}px; # Use the updated font_size
                color: #333;
                width: {self.width-10}px; 
                padding: 10px 0;
                word-wrap: break-word;
            }}
            li {{
                margin-bottom: 5px;
                line-height: 1.5;
            }}
            p {{
                line-height: 1.5;
            }}

        </style>
        </head>
        <body>{html_body}</body>
        </html>
        """
        return html

    def _calculate_image_height(self, text):
        lines = text.split('\n')
        return len(lines) * self.font_size * 2 + 150

    def generate_image(self, fate, output_file='output.png'):
        dedent_fate = textwrap.dedent(fate)
        html = self._build_html(dedent_fate)
        image_height = int(self._calculate_image_height(dedent_fate))
        hti = Html2Image(size=(self.width, image_height))
        with tempfile.TemporaryDirectory() as tmpdir:
            hti.output_path = tmpdir
            hti.screenshot(html_str=html, save_as='temp.png')
            os.rename(os.path.join(tmpdir, 'temp.png'), output_file)
        return output_file