import os
import requests
import logging

from requests import Response
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# creating the logger object
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(log_format)
logger.addHandler(sh)

# load config details
with open('config.json', 'r') as f:
    config_params = f.read()

# Initializes the app with the bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def configure_api(host: str, job_id: int, auth_token: str) -> str:
    """Configure the url of API endpoint"""
    logger.info("Configuring the API Endpoint...")
    api_endpoint = f"{host}/api/11/job/{job_id}/run?authtoken={auth_token}"
    logger.debug(f"Configured API Endpoint URL: {api_endpoint}")
    return api_endpoint


def call_api(**kwargs) -> Response:
    """Makes an API call"""
    try:
        logger.info("fetching the 'host' and 'job_id' from the config file...")
        host = kwargs.get("host")
        job_id = kwargs.get("job_id")
        logger.debug(f"host: {host}, job_id: {job_id}")
        url = configure_api(host=host, job_id=job_id, auth_token=os.environ.get("AUTH_TOKEN_RUNDECK"))
        logger.debug(f"Making an api call to {url}")
        response: Response = requests.post(url=url)
        logger.debug(f"Response status_code: {response.status_code}")
        return response

    except Exception as e:
        logging.exception("Exception, Failed to make API call")


# monitor tomcat server
@app.command("/tomcat")
def run_job(ack, respond, command):
    """Makes an API call to run a job in Rundeck"""
    ack()
    respond(f"Command: {command['text']}")
    logger.debug("Executing the rundeck job through API call...")
    call_api()


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()