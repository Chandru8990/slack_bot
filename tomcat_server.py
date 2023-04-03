import os
import requests
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from requests import Response

# creating the logger object
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(log_format)
logger.adHandler(sh)

rundeck_auth_token = os.environ.get("RUNDECK_AUTHORIZATION_TOKEN")

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# check the tomcat server
@app.command("/tomcat")
def check_tomcat(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")
    
def configure_rundeck_api(uri: str, auth_token: str) -> str:
    """Configure the url of Rundeck API Endpoint"""
    logger.debug(f"URI: {uri}")
    api_endpoint = f"{uri}?auth_token={auth_token}"
    logger.debug(f"API Endpoint URL: {api_endpoint}")
    return api_endpoint
    
    
def rundeck_connection(uri):
    try:
        response: Response = requests.post(url=url)
        logger.debug(f"{response.status_code}")
    except Exception as e:
        logging.exception("Exception occured")
	
if __name__ == "__main__":
SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()