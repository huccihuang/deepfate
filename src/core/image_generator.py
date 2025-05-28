import math
import os
import tempfile
import textwrap
import tomllib
from pathlib import Path

import markdown2
from html2image import Html2Image

# 加载TOML配置
def load_config():
    config_path = Path(__file__).parent.parent / 'config' / 'share_image_parameters.toml'
    with open(config_path, 'rb') as f:  # tomllib 需要以二进制模式读取文件
        return tomllib.load(f)

# 获取配置
CONFIG = load_config()

class HtmlStyleBuilder:
    def __init__(self):
        self.font_path = Path(__file__).parent.parent.parent / CONFIG['assets']['font_path']
        self.font_family = CONFIG['image']['font_family']
        self.font_size = CONFIG['image']['font_size']
        self.qr_code_path = Path(__file__).parent.parent.parent / CONFIG['assets']['qr_code_path']

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
        qr_config = CONFIG['qr_code']
        return f'''
            <div style="text-align: center; margin: {qr_config['margin_top']}px 0 {qr_config['margin_bottom']}px;">
                <img src="file://{qr_code_abs_path}" style="width: {qr_config['width']}px; height: {qr_config['height']}px;">
                <p style="margin-top: 10px; font-size: {qr_config['caption_font_size']}px; color: {qr_config['caption_color']};">{qr_config['caption_text']}</p>
            </div>
        '''

    def build_html(self, markdown_text):
        html_body = markdown2.markdown(markdown_text)
        font_face, font_family = self._get_font_style()
        layout = CONFIG['layout']
        image = CONFIG['image']

        html = f"""
        <html>
        <head>
        <style>
            {font_face}
            body {{
                background-color: {image['background_color']};
                font-family: '{font_family}';
                font-size: {self.font_size}px;
                color: {image['text_color']};
                padding: {layout['padding']['top']}px {layout['padding']['right']}px;
                word-wrap: break-word;
                position: relative;
            }}
            li {{
                margin-bottom: {layout['list_margin_bottom']}px;
                line-height: {layout['line_height_ratio']};
            }}
            p {{
                line-height: {layout['line_height_ratio']};
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
    def __init__(self):
        self.width = CONFIG['image']['width']
        self.html_builder = HtmlStyleBuilder()

    def _calculate_image_height(self, text):
        height_config = CONFIG['layout']['height_calculation']
        
        # 计算实际的文本宽度（考虑容器宽度和padding）
        available_width = self.width - height_config['side_padding']
        
        # 使用配置中的行高比例
        line_height_ratio = height_config['line_height_ratio']
        
        # 计算每行能容纳的大概字符数（假设中文字符宽度约等于字体大小）
        chars_per_line = available_width // self.html_builder.font_size
        
        # 分割文本并计算实际行数
        total_lines = 0
        for paragraph in text.split('\n'):
            # 计算这段文字需要的行数（向上取整）
            if paragraph.strip():  # 忽略空行
                lines_needed = math.ceil(len(paragraph) / chars_per_line)
                total_lines += lines_needed
            else:
                total_lines += 1  # 空行也算一行
        
        # 计算总高度：行数 * 行高 + 上下padding
        base_height = total_lines * self.html_builder.font_size * line_height_ratio
        total_height = base_height + height_config['padding_top'] + height_config['padding_bottom'] + CONFIG['qr_code']['height'] + 100
        
        # 确保高度不小于最小高度
        return max(int(total_height), height_config['min_height'])

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