from tkinter import *
from DefaultRoomCreator import DefaultRoomCreator

class ChatScreen():
    def __init__(self, main_frame=None, room_repo=None):
        self.room_repo = room_repo
        self.main_frame = main_frame
        self.listbox = None
        self.join_window = None
        self.buttons_frame = None
        self.chat_frame = None
        self.write_frame = None
        self.entry_room_name = None
        self.init_grid()
        self.create_chat_screen()
        self.create_write_frame()
        self.create_buttons()

    def init_grid(self):
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.chat_frame = Frame(self.main_frame, bg='white', width=720, height=800, padx=3, pady=3)
        self.write_frame = Frame(self.main_frame, width=800, height=40, padx=3, pady=3)
        self.buttons_frame = Frame(self.main_frame, width=800, height=40, padx=3, pady=3)
        self.chat_frame.grid(row=1, sticky="nsew")
        self.write_frame.grid(row=2, sticky="sew")
        self.buttons_frame.grid(row=3, sticky="sew")

    def create_write_frame(self):
        self.write_frame.grid_columnconfigure(1, weight=1)
        write_frame_button = Frame(self.write_frame, width=800, height=40, padx=3, pady=3)
        write_frame_text = Frame(self.write_frame, width=800, height=40, padx=3, pady=3)
        Button(self.write_frame, text=' Send ', command=self.on_send_message).grid(row=0, column=0, padx=7, pady=2, sticky="nsew")
        Entry(self.write_frame, bd=5).grid(row=0,column=1, padx=7, pady=2, sticky="sew")

    def create_buttons(self):
        Button(self.buttons_frame, text=' Join room ', command=self.on_wants_join).grid(row=3, padx=7, pady=2, sticky="nsew")

    def create_chat_screen(self):
        scrollbar = Scrollbar(self.chat_frame, orient=VERTICAL)
        self.listbox = Listbox(self.chat_frame, borderwidth=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        self.listbox.grid(row=1, padx=7, pady=2, sticky="nsew")
        self.listbox.insert(END, "No data in room.")
        scrollbar.config(command=self.listbox.yview)

    def on_send_message(self):
        print("sending message to room")

    def on_wants_join(self):
        print("joining room")
        self.join_window = Tk()
        self.join_window.title('Joining room')
        frame = Frame(self.join_window)
        Label1 = Label(self.join_window, text='Room:')
        Label1.pack(padx=15, pady=5)
        self.entry_room_name = Entry(self.join_window, bd=5)
        self.entry_room_name.pack(padx=15, pady=5)
        btn = Button(frame, text=' Join ', command=self.on_join)
        btn.pack(side=RIGHT, padx=5)
        frame.pack(padx=100, pady=19)
        self.join_window.mainloop()

    def on_join(self):
        room = DefaultRoomCreator().create(self.entry_room_name.get(), )
        self.room_repo.add(room)
        room.start(self.on_new_messages)
        self.join_window.destroy()

    def on_new_messages(self,data):
        self.listbox.insert(END, data)