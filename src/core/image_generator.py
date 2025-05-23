import markdown2
from html2image import Html2Image
import tempfile
import os

class ImageGenerator:
    def __init__(self, font_family='Arial', font_size=20, font_path=None):
        self.font_family = font_family
        self.font_size = font_size
        self.font_path = "https://github.com/lxgw/kose-font/releases/download/v3.120/XiaolaiSC-Regular.ttf"

    def _build_html(self, markdown_text):
        html_body = markdown2.markdown(markdown_text)
        font_face = ""
        if self.font_path:
            abs_path = os.path.abspath(self.font_path)
            font_face = f"""
            @font-face {{
                font-family: 'CustomFont';
                src: url('file://{abs_path}');
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
                font-size: {self.font_size}px;
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
        html = self._build_html(text)
        hti = Html2Image()
        with tempfile.TemporaryDirectory() as tmpdir:
            hti.output_path = tmpdir
            hti.screenshot(html_str=html, save_as='temp.png')
            os.rename(os.path.join(tmpdir, 'temp.png'), output_file)
        return output_file