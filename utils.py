import re

def get_conversation_snippet(content, max_words=3, max_chars=30):
    """
    Get a snippet of the conversation content for display in the sidebar.
    
    :param content: The full content of the message
    :param max_words: Maximum number of words to include in the snippet
    :param max_chars: Maximum number of characters to include in the snippet
    :return: A string containing the snippet
    """
    words = content.split()
    snippet = ' '.join(words[:max_words])
    
    if len(snippet) > max_chars:
        snippet = snippet[:max_chars-3] + '...'
    elif len(words) > max_words:
        snippet += '...'
    
    return snippet

def format_message_for_display(msg):
    """
    Format a message for display in the UI.
    
    :param msg: A dictionary containing the message information
    :return: A formatted string ready for display
    """
    role = msg['role'].capitalize()
    content = msg['content']
    
    if 'timestamp' in msg:
        formatted_time = format_timestamp(msg['timestamp'])
        return f"**{role}** ({formatted_time}):\n\n{content}"
    else:
        return f"**{role}**:\n\n{content}"

def format_timestamp(timestamp):
    """
    Format a timestamp string into a more readable format.
    
    :param timestamp: A string timestamp in the format "YYYYMMDDHHMMSS"
    :return: A formatted string like "YYYY-MM-DD HH:MM:SS"
    """
    return f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[8:10]}:{timestamp[10:12]}:{timestamp[12:14]}"

def clean_text(text):
    """
    Clean and normalize text input.
    
    :param text: Input text string
    :return: Cleaned text string
    """
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text

def count_words(text):
    """
    Count the number of words in a text string.
    
    :param text: Input text string
    :return: Number of words
    """
    return len(text.split())

def truncate_text(text, max_length=100):
    """
    Truncate text to a maximum length.
    
    :param text: Input text string
    :param max_length: Maximum length of the output string
    :return: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'