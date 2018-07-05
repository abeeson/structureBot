# structureBot
EVE Structure Bot to check fuel levels for a corporation, and report them to slack when low

## Prereqs
* Python3
* Python3 Requests
* Python3 configparser

## Usage
to use this you will need to get a valid ESI refresh_token, as well as setting up a slack bot, and adding it into the channel you want to use

### ESI token
1. go here: https://login.eveonline.com/oauth/authorize/?response_type=code&redirect_uri=https://localhost/na&client_id=e29f9ccc16094478859fcc6a9767b836&scope=esi-mail.read_mail.v1 esi-universe.read_structures.v1 esi-corporations.read_structures.v1 esi-corporations.read_starbases.v1 and authorise your EVE account with this tool
2. run the get_token.py script included here, with the code you received from step 1 as the only argument. i.e. python3 get_token.py CODE_HERE. If you did this right, the script will print your refresh_token for you to insert into the configuration file

### Slack token
Go to your slack account, under custom integrations, and create a bot. Save the token into the configuration, and ensure you invite the bot into a channel and set that channel name in the configuration as well. 
