# Introduction

**girl_scouts_year_planner** is a python tool to perform annual event planning with the power of Google Gemini model. Since it was written quickly for the sole purpose of planning for my Girl Scouts troops in Northern California, the tool is anchored on fetching the web contents from GSNorCal's event calendar site. See main.py file to update the filters and adjust prompts to fit your planning need!

# Setup and Installation 

## Setting up Gemini API KEY

To use the API, we have to first get an API key that you can can from here: https://ai.google.dev/tutorials/setup

After that click on “Get an API key” button and then click on “Create API key in new project”.

Copy the API key and set it as an environment variable `GEMINI_API_KEY`. 

## Dependencies of Gemini

You will need to install the following: 

    % pip install google-generativeai pyttsx3 opencv-python
    % pip install -q -U google-genai 

You will will need to install "Python 3.10" or higher to use Gemini.

## Other Requirements

The following modules are needed for heavy json rendering web content fetches:

    % pip install requests-html
    % pip install lxml_html_clean

