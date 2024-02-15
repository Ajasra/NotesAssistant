import re
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup

class MyHTMLParser(HTMLParser):
    """
    Custom HTML Parser class that extends the built-in HTMLParser class.
    This class is used to parse HTML content.
    """
    def __init__(self):
        super().__init__()
        self.stack = []

    def handle_starttag(self, tag, attrs):
        """
        Method to handle start tags. It adds the tag to the stack.
        """
        self.stack.append(tag)

    def handle_endtag(self, tag):
        """
        Method to handle end tags. It removes the tag from the stack.
        """
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

def format_text_to_html(text):
    """
    Function to format markdown text to HTML.

    Parameters:
    text (str): The text to be formatted.

    Returns:
    str: The formatted text.
    """
    # Replace markdown syntax with HTML tags
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'^\*(.*)$', r'⚪ \1', text, flags=re.MULTILINE)

    text = re.sub(r'^#{2,}(.*)$', lambda m: '{}'.format(m.group(1).strip().upper()), text, flags=re.MULTILINE)
    text = re.sub(r'^#(.*)$', lambda m: '<b>{}</b>'.format(m.group(1).strip().upper()), text, flags=re.MULTILINE)

    # Replace markdown code blocks with HTML pre tags
    # Add more languages as needed
    language_tags = {
        'python': '<pre language="python">',
        'javascript': '<pre language="javascript">',
        'java': '<pre language="java">',
    }
    end_tag = '</pre>'

    # Extract the language from the code block delimiter
    while '```' in text:
        # Extract the language from the code block delimiter
        match = re.search(r'```(\w+)', text)
        if match:
            language = match.group(1)
            if language in language_tags:
                start_tag = language_tags[language]
                text = text.replace("```" + language, start_tag, 1)
                text = text.replace("```", end_tag, 1)
            else:
                text = text.replace("```" + language, '<code>', 1)
                text = text.replace("```", '</code>', 1)
        else:
            text = text.replace("```", '<code>', 1)
            text = text.replace("```", '</code>', 1)

    # Replace markdown links with HTML a tags
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    # Parse the text with the custom HTML parser
    parser = MyHTMLParser()
    parser.feed(text)

    # Remove unmatched tags
    if parser.stack:
        for tag in parser.stack:
            text = re.sub(r'<{}[^>]*>'.format(tag), '', text)

    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    return text

def find_links_in_text(text):
    """
    Function to find all URLs in a text.

    Parameters:
    text (str): The text to search for URLs.

    Returns:
    list: A list of URLs found in the text.
    """
    # Regular expression to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # Find all URLs in the text
    urls = url_pattern.findall(text)

    return urls

def get_main_text_from_url(url):
    """
    Function to get the main text from a URL.

    Parameters:
    url (str): The URL to get the main text from.

    Returns:
    tuple: A tuple containing the main text and the main image URL.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main text of the page. This will depend on the structure of the webpage.
    main_text_elements = soup.find_all(['p', 'article', 'section', 'main'])

    # Extract the text from the main_text elements
    main_text = [element.get_text() for element in main_text_elements]
    main_text = [text for text in main_text if text.strip()]
    # delete all the empty strings
    main_text = list(filter(None, main_text))

    # Find the meta description tag
    meta_description_tag = soup.find('meta', attrs={'name': 'description'})
    # Extract the content of the meta description tag
    meta_description = meta_description_tag['content'] if meta_description_tag else None

    # Find the main image tag
    main_image_tag = soup.find('meta', attrs={'property': 'og:image'})
    # Extract the content of the main image tag
    main_image_url = main_image_tag['content'] if main_image_tag else ""

    main_text = "\n".join(main_text)
    # Clean up the text
    main_text = re.sub(r'\s+', ' ', main_text).strip()

    result = """
    META DESCRIPTION: {}
    PAGE CONTENT: {}
    """.format(meta_description, main_text)

    return result, main_image_url

def clean_text(text):
    """
    Function to clean a text.

    Parameters:
    text (str): The text to be cleaned.

    Returns:
    str: The cleaned text.
    """
    # if text are array, convert to string
    if not isinstance(text, str):
        text = ', '.join(text)
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Replace "None" with an empty string
    text = text.replace("None", "")
    return text