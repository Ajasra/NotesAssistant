import os
import requests

from dotenv import load_dotenv

from gemini_api import handle_gemini_model

load_dotenv()
NOTION_API = os.getenv("NOTION_API")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_API,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def add_notion_page(title, content="", summary="", tags="", image="", link=""):
    create_url = "https://api.notion.com/v1/pages"
    print(title, content, summary, tags, image, link)

    if summary == "":
        summary = handle_gemini_model("Summarize next text. Reply only summary: " + title)
    if tags == "":
        tags = handle_gemini_model("Give me tags for the text below. Reply in format 'tag1, tag2, tag3, ..': " + title)

    data = {
        "Name": {"title": [{"text": {"content": title}}]},
        "summary": {"rich_text": [{"text": {"content": summary}}]},
        "tags": {"rich_text": [{"text": {"content": tags}}]},
        "link": {"rich_text": [{"text": {"content": link}}]},
    }

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)

    if res.status_code == 200:
        return title + (" added to Notion : "
                        "" + summary + ""
                        "" + tags)
    else:
        return "Error: " + res.text
