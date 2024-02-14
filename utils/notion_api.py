import os
import requests
from dotenv import load_dotenv
from gemini_api import handle_gemini_model
from messages import PROCESSED

# Load environment variables from .env file
load_dotenv()

# Get environment variables
NOTION_API = os.getenv("NOTION_API")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
FILESERVER = os.getenv("FILESERVER")

# Set headers for Notion API
headers = {
    "Authorization": "Bearer " + NOTION_API,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def add_notion_page(title, summary="", tags="", image="", link=""):
    """
    Function to add a page to Notion.

    Parameters:
    title (str): The title of the page.
    summary (str, optional): The summary of the page. Defaults to "".
    tags (str, optional): The tags for the page. Defaults to "".
    image (str, optional): The image for the page. Defaults to "".
    link (str, optional): The link for the page. Defaults to "".

    Returns:
    str: A message indicating whether the page was added successfully or an error occurred.
    """

    # Notion API endpoint to create a new page
    create_url = "https://api.notion.com/v1/pages"

    # Process the title using the Gemini model
    processed = handle_gemini_model(PROCESSED + title)
    try:
        processed = eval(processed)
    except Exception as e:
        print(e)
        processed['summary'] = ""
        processed['tags'] = ""

    # Prepare the data for the new page
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "mytext": {"title": [{"text": {"content": title}}]},
            "summary": {"rich_text": [{"text": {"content": processed['summary']}}]},
            "tags": {"rich_text": [{"text": {"content": processed['tags']}}]},
        }
    }

    # If an image is provided, add it to the page
    if image != "":
        image = FILESERVER + image
        data["properties"]["image"] = {
            "type": "files",
            "files": [
                {
                    "type": "external",
                    "name": "Example File",
                    "external": {"url": image}
                }
            ]
        }

    # If a link is provided, add it to the page
    if link != "":
        data["properties"]["link"] = {
            "type": "url",
            "url": link
        }

    # Send a POST request to the Notion API to create the new page
    res = requests.post(create_url, headers=headers, json=data)

    # If the request was successful, return a success message
    # Otherwise, return an error message
    if res.status_code == 200:
        return title + (" added to Notion : "
                        "" + summary + ""
                        "" + tags)
    else:
        return "Error: " + res.text