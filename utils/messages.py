WELCOME_MESSAGE = "Hello"

HELP_MESSAGE = ""

NEW_CONVERSATION_MESSAGE = "Start new conversation"

PROCESSED = """
- Give a short one paragraph summary for the next text and tags. 
- if there url is provided, the summary will be generated PAGE CONTENT and META DESCRIPTION
- if not sure about the tags, just leave them empty
- if page content is empty, the summary will be generated from the title
- if the title only are link, leave summary and tags empty
- Reply in the json format:
{
    "summary": "summary",
    "tags": "tag1, tag2, tag3, ..."
}

TEXT:
"""