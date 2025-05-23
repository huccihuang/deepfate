import os
import tempfile
import textwrap
from pathlib import Path
import markdown2
from html2image import Html2Image

class ImageGenerator:
    def __init__(self, font_family='Arial', font_size=40, font_path=None): # Increased default font_size
        self.font_family = font_family
        self.font_size = font_size
        self.font_path = Path(__file__).parent.parent.parent / 'assets' / 'XiaolaiSC-Regular.ttf'

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
                padding: 20px;
                line-height: 1.6;
                color: #333;
            }}
        </style>
        </head>
        <body>{html_body}</body>
        </html>
        """
        return html

    def generate_image(self, name, fate, output_file='output.png'):
        text = f'''
        # {name} 的命理分析

        {fate}
        '''
        dedent_text = textwrap.dedent(text)
        html = self._build_html(dedent_text)
        print(html)
        hti = Html2Image()
        with tempfile.TemporaryDirectory() as tmpdir:
            hti.output_path = tmpdir
            hti.screenshot(html_str=html, save_as='temp.png')
            os.rename(os.path.join(tmpdir, 'temp.png'), output_file)
        return output_file