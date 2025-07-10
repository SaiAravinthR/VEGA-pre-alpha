import logging
from livekit.agents import function_tool, RunContext # type: ignore
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import os
import smtplib
import asyncio
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()   
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}." 

@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."    


@function_tool()
def send_email(
    to_email: str,
    subject: str,
    message: str
) -> str:
    try:
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            return "FAIL: Missing Gmail credentials"

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = gmail_user
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, [to_email], msg.as_string())
        server.quit()

        return f"✅ Sent email to {to_email}"

    except Exception as e:
        return f"❌ Error: {str(e)}"
