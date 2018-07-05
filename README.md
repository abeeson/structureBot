# structureBot
EVE Structure Bot to check fuel levels for a corporation, and report them to slack when low

## Prereqs
* Python3
* Python3 Requests
* Python3 configparser

## Usage
to use this you will need to get a valid ESI refresh_token, as well as setting up a slack bot, and adding it into the channel you want to use

## Required ESI roles
This script requires ESI grants for the following:
* esi-mail.read_mail.v1 - required for notifications i think, still testing this
* esi-universe.read_structures.v1 - required to get details about your structures for names (not in corp ESI, see below)
* esi-corporations.read_structures.v1 - required to get a list of structures that your corporation has - Unfortunately doesn't contain names
* esi-corporations.read_starbases.v1 - Allows access to legacy POS data for POS fuel levels

### ESI token
1. go here: https://login.eveonline.com/oauth/authorize/?response_type=code&redirect_uri=https://localhost/na&client_id=e29f9ccc16094478859fcc6a9767b836&scope=esi-mail.read_mail.v1%20esi-universe.read_structures.v1%20esi-corporations.read_structures.v1%20esi-corporations.read_starbases.v1 and authorise your EVE account with this tool
2. Make a note of the link you get back - It won't work, but contains a block in the URL containing the code we need for step 3, so don't close it.
3. Within 5 minutes, run the get_token.py script included here, with the code you received from step 1 as the only argument. i.e. python3 get_token.py CODE_HERE. If you did this right, the script will print your refresh_token for you to insert into the configuration file, if something was wrong the script should print the error for you

### Slack token
Go to your slack account, under custom integrations, and create a bot. Save the token into the configuration, and ensure you invite the bot into a channel and set that channel name in the configuration as well. 
