import tkinter as tk
from tkinter import ttk
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF
import rtmidi

class DrumPadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drum Pad")
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        self.portnumber = 1

        # Define the drum pad layout
        self.drum_pads = [
            ["Kick", "Snare", "Hi-Hat", "Crash"],
            ["Tom 1", "Tom 2", "Tom 3", "Ride"],
            ["Shaker", "Tambourine", "Cowbell", "Clap"]
        ]

        # Define the MIDI note numbers for each drum pad
        self.note_numbers = [
            [56, 57, 58, 59],
            [52, 53, 54, 55],
            [48, 49, 50, 51]
        ]

        # Define the keyboard shortcuts for each drum pad
        self.keyboard_shortcuts = {
            'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3),
            'a': (1, 0),'s': (1, 1), 'd': (1, 2), 'f': (1, 3),
            'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3)
        }

        self.create_widgets()
        self.bind_keyboard_shortcuts()

    def create_widgets(self):
        # Create a Tkinter window
        self.root = tk.Tk()

        # Create a MIDI output port
        if self.available_ports:
            self.midiout.open_port(self.portnumber)
        else:
            self.midiout.open_virtual_port("Drum Pad")

        # Create the drum pad buttons
        for i, row in enumerate(self.drum_pads):
            for j, pad in enumerate(row):
                button = tk.Button(self.root, command=lambda x=i, y=j: self.send_note(x, y), height=3, width=10, bd=3, bg='#1a1d1e', relief='raised')
                button.grid(row=i, column=j)

        # Create a port selection dropdown
        self.port_var = tk.StringVar()
        self.port_var.set(self.available_ports[0])
        port_menu = ttk.OptionMenu(self.root, self.port_var, *self.available_ports, command=self.change_port)
        port_menu.grid(row=3, column=0)

    def bind_keyboard_shortcuts(self):
        for key, (x, y) in self.keyboard_shortcuts.items():
            self.root.bind(key, lambda event, x=x, y=y: self.send_note(x, y))

    def send_note(self, x, y):
        note_number = self.note_numbers[x][y]
        self.midiout.send_message([NOTE_ON, note_number, 100])
        self.root.after(100, lambda: self.midiout.send_message([NOTE_OFF, note_number, 100]))

    def change_port(self, value):
        self.midiout.close_port()
        self.portnumber = self.available_ports.index(value)
        self.midiout.open_port(self.portnumber)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DrumPadApp(tk.Tk())
    app.run()