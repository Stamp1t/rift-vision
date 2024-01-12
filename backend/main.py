import obs
import handle_settings as hs
import league_data as lg
import app
import gui


def start_script():
    """ Starts the script """

    settings = hs.get_data()
    gui.create_gui(settings)
    client = obs.init_vars(settings)
    settings = hs.get_data()
    obs.init_sources(settings, client)
    print("INITIALISING DATA...")
    matches_dict, player_data = lg.create_initial_player_data(settings)
    app.start(player_data, matches_dict, client)


if __name__ == "__main__":
    start_script()
