import os
import tempfile
import textwrap
from pathlib import Path
import markdown2
from html2image import Html2Image

class HtmlStyleBuilder:
    def __init__(self, font_path=None, font_family='Arial', font_size=30):
        self.font_path = font_path
        self.font_family = font_family
        self.font_size = font_size
        self.qr_code_path = Path(__file__).parent.parent.parent / 'assets' / 'deepfate_qr_code.png'

    def _get_font_style(self):
        font_face = ""
        if self.font_path:
            font_abs_path = self.font_path.resolve()
            font_face = f"""
            @font-face {{
                font-family: 'CustomFont';
                src: url('file://{font_abs_path}');
            }}
            """
            font_family = 'CustomFont'
        else:
            font_family = self.font_family

        return font_face, font_family

    def _get_qr_code_html(self):
        qr_code_abs_path = self.qr_code_path.resolve()
        return f'''
            <div style="text-align: center; margin: 20px 0;">
                <img src="file://{qr_code_abs_path}" style="width: 200px; height: 200px;">
                <p style="margin-top: 10px; font-size: 16px; color: #666;">扫码获取我的结果</p>
            </div>
        '''

    def build_html(self, markdown_text):
        html_body = markdown2.markdown(markdown_text)
        font_face, font_family = self._get_font_style()

        html = f"""
        <html>
        <head>
        <style>
            {font_face}
            body {{
                background-color: #FFFEF8;
                font-family: '{font_family}';
                font-size: {self.font_size}px;
                color: #333;
                padding: 50px 50px;
                word-wrap: break-word;
                position: relative;
            }}
            li {{
                margin-bottom: 5px;
                line-height: 1.5;
            }}
            p {{
                line-height: 1.5;
            }}
            .qr-code {{
                position: absolute;
                bottom: 20px;
                right: 20px;
                width: 100px;
                height: 100px;
            }}
        </style>
        </head>
        <body>
            {html_body}
            {self._get_qr_code_html()}
        </body>
        </html>
        """
        return html


class ImageGenerator:
    def __init__(self, font_family='Arial', font_size=30, font_path=None, width=1080):
        self.width = width
        self.html_builder = HtmlStyleBuilder(
            font_path=Path(__file__).parent.parent.parent / 'assets' / 'XiaolaiSC-Regular.ttf',
            font_family=font_family,
            font_size=font_size
        )

    def _calculate_image_height(self, text):
        lines = text.split('\n')
        return len(lines) * self.html_builder.font_size * 2 + 300

    def generate_image(self, fate, output_file='output.png'):
        try:
            dedent_fate = textwrap.dedent(fate)
            html = self.html_builder.build_html(dedent_fate)
            image_height = int(self._calculate_image_height(dedent_fate))
            hti = Html2Image(size=(self.width, image_height))
            with tempfile.TemporaryDirectory() as tmpdir:
                hti.output_path = tmpdir
                temp_file = os.path.join(tmpdir, 'temp.png')
                hti.screenshot(html_str=html, save_as='temp.png')
                import shutil
                shutil.copy2(temp_file, output_file)
            return output_file
        except Exception as e:
            raise Exception(f"生成图片时发生错误：{str(e)}")