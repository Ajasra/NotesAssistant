from notion_api import add_notion_page

add_notion_page("""If the new page is a child of an existing page,title is the only valid property in the properties body param.

If the new page is a child of an existing database, the keys of the properties object body param must match the parent database's properties.

This endpoint can be used to create a new page with or without content using the children option. To add content to a page after creating it, use the Append block children endpoint.""")