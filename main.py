import httpx
import pathlib
import sys

from google import genai
from google.genai import types
from google.genai.types import Tool, GenerateContentConfig
from requests_html import HTMLSession

# Search range parameters for the Girl Scouts NorCal events calendar site.
OPEN_SPOTS="6"
START_DATE="2025-09-01"
MIN_AGE="9"
BASE_URL = f"https://anc.apm.activecommunities.com/gsnorcal/activity/search?onlineSiteId=0&activity_select_param=2&open_spots={OPEN_SPOTS}&min_age={MIN_AGE}&date_after={START_DATE}&viewMode=list"

PROMPT_8G = f"""
You are a Girl Scout troop leader for an 8th grade Cadette troop of {OPEN_SPOTS} girls.

It is September 1, 2025 and you are planning for troop outings for the 2025-26 school year,
which starts in September and ends in June. The plan should consist of no more than 2 outings
a month. The event should be within 60 miles from Mountain View California. Scouts are not
interested in attending Award Q&A sessions.

Provide a possible plan for the year.
"""

PROMPT_5G = f"""
You are a Girl Scout troop leader for a 5th grade Junior troop of {OPEN_SPOTS} girls.

It is September 1, 2025 and you are planning for troop outings for the 2025-26 school year,
which starts in September and ends in June. The plan should consist of no more than 2 outings
a month. The event should be within 60 miles from Mountain View California. Scouts are not
interested in attending Award Q&A sessions.

Provide a possible plan for the year.
"""

PROMPT_COMMON_PLAN = """
You are a Girl Scout troop leader for a 5th grade Junior troop and an 8th grade Cadette troop.

It is September 1, 2025 and you are planning for troop outings for the 2025-26 school year,
which starts in September and ends in June. The plan should consist of no more than 2 outings
a month. The event should be within 60 miles from Mountain View California. Events that are
offered for both Junior and Cadette level should be prioritized. Scouts are not
interested in attending Award Q&A sessions.

Provide a possible plan for the year, listing name of the event, date, location, activity
number, and a brief description.
"""

def fetch_and_save_page(url, filename):
    """
    Fetches a URL, renders its content and saves to a local file.

    Args:
        url (str): The URL of the webpage to fetch.
        filename (str): The name of the file to save the content to.
    """
    try:
        session = HTMLSession()
        print(f"Fetching URL: {url}")

        # Make the GET request.
        response = session.get(url)
      
        # Render the page and scroll down 5 times
        print("Rendering JavaScript content...")
        response.html.render(scrolldown=5, sleep=3)

        # Get the rendered HTML.
        rendered_html = response.html.html

        # Write the content to a local file.
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(rendered_html)

        print(f"Successfully saved HTML content to '{filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Note: Required installations:
    #    % pip install requests-html
    #    % pip install lxml_html_clean
    output_filename = 'output.html'
    fetch_and_save_page(BASE_URL, output_filename)

    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()
    model_id = "gemini-2.5-flash"

    file_path = pathlib.Path(output_filename)
    sample_file = client.files.upload(
      file=file_path,
    )
    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[sample_file, PROMPT_COMMON_PLAN])

    print(response.text)
