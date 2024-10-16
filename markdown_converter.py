import streamlit as st
import re

def convert_to_markdown(text):
    """
    Convert plain text to markdown, preserving existing markdown formatting.
    """
    # Split the text into lines
    lines = text.split('\n')
    markdown_lines = []
    in_list = False
    in_code_block = False

    for line in lines:
        # Preserve existing markdown headings
        if re.match(r'^#{1,6}\s', line):
            markdown_lines.append(line)
        # Preserve existing markdown lists
        elif line.strip().startswith(('-', '*', '1.')):
            markdown_lines.append(line)
        # Preserve code blocks
        elif line.strip().startswith('```'):
            in_code_block = not in_code_block
            markdown_lines.append(line)
        # Preserve lines within code blocks
        elif in_code_block:
            markdown_lines.append(line)
        # Convert plain text paragraphs to markdown paragraphs
        elif line.strip():
            markdown_lines.append(line + '  ')
        # Preserve empty lines
        else:
            markdown_lines.append(line)

    # Join the lines back together
    markdown_text = '\n'.join(markdown_lines)

    # Convert **text** to bold if not already formatted
    markdown_text = re.sub(r'(?<!\*)\*\*(?![\s\*])(.+?)(?<![\s\*])\*\*(?!\*)', r'**\1**', markdown_text)

    # Convert *text* to italic if not already formatted
    markdown_text = re.sub(r'(?<!\*)\*(?![\s\*])(.+?)(?<![\s\*])\*(?!\*)', r'*\1*', markdown_text)

    return markdown_text