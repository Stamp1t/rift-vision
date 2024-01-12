# Rift Vision

## Overview
Welcome to **Rift Vision** – an automatically updating overlay designed for League of Legends streamers. This project aims to enhance the streaming experience by providing dynamic, real-time information directly within the streaming interface.


## Technologies Used
### Languages
- Python
- JavaScript
- HTML
- CSS

### Modules
- websockets
- obswebsocket

## How to Set Things up
To get started with Rift Vision, please follow these steps:

1. **Install OBSWebSocket:**
   - First, you need to download and install OBSWebSocket. It's a crucial component that enables real-time communication between OBS Studio and Rift Vision. You can download it [here]([https://github.com/Palakis/obs-websocket](https://github.com/obsproject/obs-websocket/releases)).

2. **Download Rift Vision:**
   - Next, download the Rift Vision application. (Link to be added by the project maintainer)

3. **Install OBS:**
   - You will need to use OBS as your streaming software.

## Getting Started
Once you have installed OBSWebSocket, you should locate the WebSocket server settings within OBS under "Tools". Ensure that the "Enable WebSockets Server" option is checked. Then, remember your server port and set a password.

After these settings are configured in OBS:

1. Run the `Rift Vision.exe` file.
2. A settings window will open where you need to enter the following information:
   - **Riot ID:** Enter your Riot ID, e.g., Player123#EUW.
   - **Queue Type:** Select the desired queue type.
   - **Riot API Key:** Enter your Riot API key, which can be found [here](https://developer.riotgames.com/). Note that the Riot API Key must be renewed every 24 hours, which can be done on the same page using the "Regenerate API Key" option.
   - **OBS Server Port:** Enter the server port noted from the OBS settings.
   - **OBS Server Password:** Enter the password you set in OBS.
   - **Scene Name:** Enter the name of the OBS scene where you want to add the overlay.
3. After entering all the required information, click 'Save' and start the program.

After a few seconds, the overlay should be shown in OBS. You can adjust the size and position according to your preferences.

*IMPORTANT:* You should always wait about 30 seconds after renewing your API Key and not start the program immediately. Also keep in mind to renew your API Key every 24 Hours because the Program will not work if the Key is outdated.
