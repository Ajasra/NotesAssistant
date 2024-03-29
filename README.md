# Telegram Bot Notion Assistant

This project is a Telegram bot designed to serve as a personal assistant for managing notes within a Notion database. It's built to enhance productivity and note-taking efficiency by automating the process of adding notes with generated summaries and tags.

## Functionality

- **Automated Note Addition:** Adds notes to the Notion database, complete with automatically generated summaries and tags.
- **Content Parsing:** Capable of parsing text, images, links, and voice inputs.
- **Image Processing:** Transcribes text from images or generates descriptions for them before uploading to the server and adding to the Notion page as a field.
- **Audio Transcription:** Uses Whisper to transcribe audio inputs.
- **Link Processing:** Parses links within texts to generate summaries and tags, including parsing meta tags and adding an image to the Notion page if mentioned in the meta tags.

This tool was initially created for personal use to consolidate notes in one place for future review. Notion serves as the main organizational tool, with the Telegram bot providing a straightforward interface for capturing anything of interest.

## Setup and Installation

1. **Clone the Code:** Start by cloning the repository to your local machine.
2. **Create your Telegram Bot Token:** Create a new bot using the [@BotFather](https://core.telegram.org/bots#6-botfather) and obtain your bot token.
3. **API Keys:** Obtain the necessary API keys:
   - [OpenAI API Key](https://platform.openai.com/account/api-keys)
   - [Google Gemini API Key](https://ai.google.dev/docs/gemini_api_overview) (Use Gemini as it's free now)
3. **Notion Setup:** Create your [Notion token](https://developers.notion.com/docs/authorization#set-up-the-auth-flow-for-a-public-integration) and set up a database with the following fields: `mytext` (Title), `tags` (Text), `summary` (Text), `image` (Files & Media), `link` (URL).
4. **Environment Variables:** Fill in the `.env` file with the required credentials and settings.
5. **Install Requirements:** Install the project dependencies.
6. **Start the Telegram Bot:** Run `python main.py` to start the bot.
7. **Start the File Server:** Run `python fileserver.py` to start the file server.

Enjoy your new Telegram bot Notion assistant!