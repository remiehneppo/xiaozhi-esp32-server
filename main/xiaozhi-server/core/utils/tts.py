import os
import re
import sys
import importlib

from config.logger import setup_logging
from core.utils.textUtils import check_emoji

logger = setup_logging()

punctuation_set = {
    "，",
    ",",  # trong + 
    "。",
    ".",  # trong + 
    "！",
    "!",  # trong + 
    "“",
    "”",
    '"',  # trong + 
    "：",
    ":",  # trong + 
    "-",
    "－",  # ký tự + trong
    "、",  # trong
    "[",
    "]",  # 
    "【",
    "】",  # trong
    "~",  # 
}

def create_instance(class_name, *args, **kwargs):
    # tạoTTS
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'providers', 'tts', f'{class_name}.py')):
        lib_name = f'core.providers.tts.{class_name}'
        if lib_name not in sys.modules:
            sys.modules[lib_name] = importlib.import_module(f'{lib_name}')
        return sys.modules[lib_name].TTSProvider(*args, **kwargs)

    raise ValueError(f"khôngcủTTS: {class_name}，kiểm tracấu hìnhcủtypelàđặtđúng")


class MarkdownCleaner:
    """
     Markdown dọn dẹp：sử dụng MarkdownCleaner.clean_markdown(text) 
    """
    # ký tự
    NORMAL_FORMULA_CHARS = re.compile(r'[a-zA-Z\\^_{}\+\-\(\)\[\]=]')

    @staticmethod
    def _replace_inline_dollar(m: re.Match) -> str:
        """
        chỉphảiđếnhoàn chỉnhcủ "$...$":
          - nhưnội bộcóký tự => đi $
          -  (/v.v.) => giữ lại "$...$"
        """
        content = m.group(1)
        if MarkdownCleaner.NORMAL_FORMULA_CHARS.search(content):
            return content
        else:
            return m.group(0)

    @staticmethod
    def _replace_table_block(match: re.Match) -> str:
        """
        khớpđếnmộtkhi/thời，hàm。
        """
        block_text = match.group('table_block')
        lines = block_text.strip('\n').split('\n')

        parsed_table = []
        for line in lines:
            line_stripped = line.strip()
            if re.match(r'^\|\s*[-:]+\s*(\|\s*[-:]+\s*)+\|?$', line_stripped):
                continue
            columns = [col.strip() for col in line_stripped.split('|') if col.strip() != '']
            if columns:
                parsed_table.append(columns)

        if not parsed_table:
            return ""

        headers = parsed_table[0]
        data_rows = parsed_table[1:] if len(parsed_table) > 1 else []

        lines_for_tts = []
        if len(parsed_table) == 1:
            # chỉcó
            only_line_str = ", ".join(parsed_table[0])
            lines_for_tts.append(f"：{only_line_str}")
        else:
            lines_for_tts.append(f"là：{', '.join(headers)}")
            for i, row in enumerate(data_rows, start=1):
                row_str_list = []
                for col_index, cell_val in enumerate(row):
                    if col_index < len(headers):
                        row_str_list.append(f"{headers[col_index]} = {cell_val}")
                    else:
                        row_str_list.append(cell_val)
                lines_for_tts.append(f" {i} ：{', '.join(row_str_list)}")

        return "\n".join(lines_for_tts) + "\n"

    # có（theosắp xếp）
    # nàytrongphải replace_xxx củphương pháptại/trongđịnh nghĩa，bằngtại/trongtrongcó thểđúngsử dụngnhững。
    REGEXES = [
        (re.compile(r'```.*?```', re.DOTALL), ''),  # 
        (re.compile(r'^#+\s*', re.MULTILINE), ''),  # 
        (re.compile(r'(\*\*|__)(.*?)\1'), r'\2'),  # 
        (re.compile(r'(\*|_)(?=\S)(.*?)(?<=\S)\1'), r'\2'),  # 
        (re.compile(r'!\[.*?\]\(.*?\)'), ''),  # 
        (re.compile(r'\[(.*?)\]\(.*?\)'), r'\1'),  # 
        (re.compile(r'^\s*>+\s*', re.MULTILINE), ''),  # sử dụng
        (
            re.compile(r'(?P<table_block>(?:^[^\n]*\|[^\n]*\n)+)', re.MULTILINE),
            _replace_table_block
        ),
        (re.compile(r'^\s*[*+-]\s*', re.MULTILINE), '- '),  # 
        (re.compile(r'\$\$.*?\$\$', re.DOTALL), ''),  # 
        (
            re.compile(r'(?<![A-Za-z0-9])\$([^\n$]+)\$(?![A-Za-z0-9])'),
            _replace_inline_dollar
        ),
        (re.compile(r'\n{2,}'), '\n'),  # nhiều
    ]

    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        vàophương pháp：có，loại bỏhoặcthay thế Markdown 
        """
        for regex, replacement in MarkdownCleaner.REGEXES:
            text = regex.sub(replacement, text)

        # điemoji
        text = check_emoji(text)

        # kiểm travăn bảnlàchovàdấu câu
        if text and all((c.isascii() or c.isspace() or c in punctuation_set) for c in text):
            # giữ lạiban đầu，trả về
            return text

        return text.strip()

def convert_percentage_to_range(percentage, min_val, max_val, base_val=None):
    """
    sẽphần trăm(-100~100)chuyển đổichochỉ địnhcủ

    Args:
        percentage: phần trăm (-100 đến 100)
        min_val: 
        max_val: 
        base_val: （tùy chọn，mặc địnhchotrong）

    Returns:
        chuyển đổisaucủ
    """
    percentage, min_val, max_val = float(percentage), float(min_val), float(max_val)
    base_val = float(base_val) if base_val is not None else (min_val + max_val) / 2

    if percentage < 0:
        # phần trăm：từ base_val hướng min_val 
        result = base_val + (base_val - min_val) * (percentage / 100)
    else:
        # phần trăm：từ base_val hướng max_val 
        result = base_val + (max_val - base_val) * (percentage / 100)

    # đảm bảokết quảtại/tronghiệu quảbên trong
    return max(min_val, min(max_val, result))
