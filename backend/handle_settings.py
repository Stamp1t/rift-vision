""" Reads and enters data to 'settings.txt' """
import os


def write_data(riot_id, match_type, riot_api_key, obs_port, obs_password, scene, server):
    """ writes given data to the file """

    # preparing data for writing to the text file
    data = (
        f"RiotId: {riot_id}\nMatch Type: {match_type}\nRiot Games API Key: {riot_api_key}\n"
        f"OBS Server Port: {obs_port}\nOBS Server Password: {obs_password}\n"
        f"Scene: {scene}\nServer: {server}"
    )

    # writing data to the text file
    with open(get_current_path()+"\\backend\\user_settings.txt", "w") as file:
        file.write(data)


def get_data():
    """ returns a dictionary containing all the data """

    result_dict = {}
    with open(get_current_path()+"\\backend\\user_settings.txt", "r") as file:
        for line in file:
            if ": " in line:
                key, value = line.split(": ", 1)
                result_dict[key.strip()] = value.strip()
    return result_dict


def get_current_path():
    """ returns current path """

    return os.getcwd()




