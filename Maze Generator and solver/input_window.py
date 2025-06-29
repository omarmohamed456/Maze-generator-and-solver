import tkinter as tk
import random

def get_maze_parameters():
    result = {} #dict

    def on_submit(): #reads input and closes input window
        # Read values from entries and apply defaults
        width_input = entries["Maze Width"].get()
        height_input = entries["Maze Height"].get()
        seed_input = entries["Seed"].get()
        delay_input = entries["Delay"].get()

        result["width"] = int(width_input) if width_input else 10
        result["height"] = int(height_input) if height_input else result["width"]
        result["seed"] = int(seed_input) if seed_input else random.randint(0, 0xFFFFFFFF)
        result["delay"] = float(delay_input) if delay_input else 0.01

        inputWindow.destroy()  # Close the input window

    # Create GUI window
    inputWindow = tk.Tk()
    inputWindow.title("Maze Parameters Input")

    fields = ["Maze Width", "Maze Height", "Seed", "Delay"]
    entries = {}

    for i, field in enumerate(fields):
        label = tk.Label(inputWindow, text=field)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w") #stick to the west side
        
        input_field = tk.Entry(inputWindow) #entry text field
        input_field.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = input_field #the filed name (label) is the key to get the input from the fields

    submit_btn = tk.Button(inputWindow, text="Submit", command=on_submit) #create button
    submit_btn.grid(row=len(fields), column=0, padx=10,pady=10, sticky="w") #set position after the fields

    inputWindow.mainloop()  #keeps Tkinter event loop running # the code doesn't continue to return unless the user exits # if the x button is used the dict remains empty so it causes a KeyError

    return result["width"], result["height"], result["seed"], result["delay"]
