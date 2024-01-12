import websockets
import asyncio
import json
import handle_settings
import league_data as lg
import obs

is_running = False


async def update_overlay(websocket, player_data, matches_dict):
    global is_running
    if not is_running:
        is_running = True
        counter = 0
        settings = handle_settings.get_data()
        while True:
            print("____________________________________")
            print(f"UPDATE ({counter + 1})")
            counter += 1
            match = lg.check_for_new_match(player_data, settings)
            if match:
                lg.update_player_data(player_data, settings, matches_dict, match)
            print("____________________________________")
            print("\n")
            await websocket.send(json.dumps(player_data))
            print("NEXT UPDATE IN 10 SECONDS:")
            await asyncio.sleep(10)


def start(player_data, matches_dict, client):
    start_server = websockets.serve(lambda websocket, path: update_overlay(websocket, player_data, matches_dict),
                                    'localhost', 6789)
    obs.refresh_browser(client, "rift-overlay")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
