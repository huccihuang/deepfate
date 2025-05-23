import os
import tempfile
import textwrap
from pathlib import Path
import markdown2
from html2image import Html2Image

class ImageGenerator:
    def __init__(self, font_family='Arial', font_size=12, font_path=None, width=300): # Increased default font_size, added width
        self.font_family = font_family
        self.font_size = font_size
        self.font_path = Path(__file__).parent.parent.parent / 'assets' / 'XiaolaiSC-Regular.ttf'
        self.width = width # Store the width

    def _build_html(self, markdown_text):
        html_body = markdown2.markdown(markdown_text)
        font_abs_path = self.font_path.resolve()
        print(font_abs_path)
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
                font-family: '{font_family}';
                font-size: {self.font_size}px; # Use the updated font_size
                /*padding: 20px;*/
                line-height: 1.6;
                color: #333;
                width: {self.width}px; 
                word-wrap:break-word;
            }}
        </style>
        </head>
        <body>{html_body}</body>
        </html>
        """
        return html

    def generate_image(self, fate, output_file='output.png'):
        dedent_fate = textwrap.dedent(fate)
        html = self._build_html(dedent_fate)
        print(html)
        hti = Html2Image(size=(self.width, 1000))
        with tempfile.TemporaryDirectory() as tmpdir:
            hti.output_path = tmpdir
            hti.screenshot(html_str=html, save_as='temp.png')
            os.rename(os.path.join(tmpdir, 'temp.png'), output_file)
        return output_file