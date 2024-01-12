""" Modul which will interact with OBS Studio """

import obswebsocket
import os


def init_vars(user_settings):
    """ creates client """

    obs_port = int(user_settings["OBS Server Port"])
    obs_password = (user_settings["OBS Server Password"])

    client = obswebsocket.obsws("localhost", obs_port, obs_password)
    client.connect()
    return client


def hide_source(source, scene, client):
    """ Hides a given source """

    client.call(obswebsocket.requests.SetSceneItemProperties(
        scene_name=scene,
        item=source,
        visible=False))


def show_source(source, scene, client):
    """ Shows a given source """

    client.call(obswebsocket.requests.SetSceneItemProperties(
        scene_name=scene,
        item=source,
        visible=True))


def refresh_browser(client, source_name):
    """ Refreshes a given browser source in obs """

    client.call(obswebsocket.requests.RefreshBrowserSource(
        sourceName=source_name
    ))


def create_source(client, scene, source_type, source_name):
    """ Will create a source and add it to a scene """

    source_types = {
        "img": "image_source",
        "text": "text_gdiplus",
        "browser": "browser_source"
    }

    source_type = source_types[source_type]
    source_settings = {"file": ""} if source_type == "img" else {"text": "loading..."}

    # create source
    try:
        client.call(obswebsocket.requests.CreateSource(sourceName=source_name, sourceKind=source_type,
                                                       sourceSettings=source_settings, sceneName=scene))
    except Exception:
        print("ERROR WHILE CREATING SOURCE")


def init_sources(user_settings, client):
    """ Will create the needed sources """

    scene = user_settings["Scene"]

    current_path_overlay = os.getcwd() + "\\overlay\\overlay.html"

    create_source(client, scene, "browser", "rift-overlay")
    client.call(obswebsocket.requests.SetSourceSettings(sourceName="rift-overlay",
                                                        sourceSettings={"url": current_path_overlay}))
