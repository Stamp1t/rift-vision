""" Creates a GUI to enter settings """

import tkinter as tk
from tkinter import ttk

from handle_settings import write_data

# Global variables for input fields
riot_id_entry = None
match_type_var = None
riot_api_entry = None
obs_port_entry = None
obs_password_entry = None
scene_entry = None


def save_data():
    """ Saves given data to a text file """

    global riot_id_entry, match_type_var, riot_api_entry, obs_port_entry, obs_password_entry, scene_entry

    # retrieving data from the input fields
    riot_id = riot_id_entry.get()
    match_type = match_type_var.get()
    riot_api_key = riot_api_entry.get()
    obs_port = obs_port_entry.get()
    obs_password = obs_password_entry.get()
    scene = scene_entry.get()

    # check if there is an empty entry
    # do not add check boxes here -> False/empty is valid for them!
    input_list = [riot_id, match_type, riot_api_key, obs_port, obs_password, scene]

    for inp in input_list:
        if not inp:
            print(f"Invalid Input!")
            return

    write_data(riot_id, match_type, riot_api_key, obs_port, obs_password, scene)

    # Printing the data for verification
    print("____________________________________________________")
    print("!Saved settings successfully:")
    print(f"Riot Id: {riot_id}")
    print(f"Match Type: {match_type}")
    print(f"Riot Games API Key: {riot_api_key}")
    print(f"OBS Server Port: {obs_port}")
    print(f"OBS Server Password: {obs_password}")
    print(f"Scene: {scene}")
    print("____________________________________________________")
    print("\n")


def create_gui(current_settings):
    """ creates the GUI layout """

    def continue_script():
        """ Starts the main script """

        root.destroy()

    global riot_id_entry, match_type_var, riot_api_entry, obs_port_entry, obs_password_entry, scene_entry

    root = tk.Tk()
    root.title("User Settings")
    root.geometry("400x300")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 10))
    style.configure("TButton", font=("Arial", 10))
    style.configure("TCheckbutton", font=("Arial", 10))

    ttk.Label(root, text="Riot ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    riot_id_entry = ttk.Entry(root)
    riot_id_entry.grid(row=0, column=1, padx=10, pady=10)
    riot_id_entry.insert(0, current_settings["RiotId"])

    ttk.Label(root, text="Match Type:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    match_type_var = tk.StringVar()
    match_type_combobox = ttk.Combobox(root, textvariable=match_type_var, state="readonly")
    match_type_combobox['values'] = ("Ranked", "Flex")
    match_type_combobox.grid(row=1, column=1, padx=10, pady=10)
    match_type_combobox.current(0)
    match_type_combobox.set(current_settings["Match Type"])

    ttk.Label(root, text="Riot Games API Key:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    riot_api_entry = ttk.Entry(root)
    riot_api_entry.grid(row=2, column=1, padx=10, pady=10)
    riot_api_entry.insert(0, current_settings["Riot Games API Key"])

    ttk.Label(root, text="OBS Server Port:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    obs_port_entry = ttk.Entry(root)
    obs_port_entry.grid(row=3, column=1, padx=10, pady=10)
    obs_port_entry.insert(0, current_settings["OBS Server Port"])

    ttk.Label(root, text="OBS Server Password:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    obs_password_entry = ttk.Entry(root)
    obs_password_entry.grid(row=4, column=1, padx=10, pady=10)
    obs_password_entry.insert(0, current_settings["OBS Server Password"])

    ttk.Label(root, text="Scene:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
    scene_entry = ttk.Entry(root)
    scene_entry.grid(row=5, column=1, padx=10, pady=10)
    scene_entry.insert(0, current_settings["Scene"])

    save_button = ttk.Button(root, text="Save", command=save_data)
    save_button.grid(row=9, column=0, columnspan=1, padx=15, pady=5)

    start_button = ttk.Button(root, text="Start", command=continue_script)
    start_button.grid(row=9, column=1, columnspan=1, padx=100, pady=5)

    root.mainloop()