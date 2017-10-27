from tkinter import *
from ChatScreen import ChatScreen

from RoomRepository import RoomRepository


class FlowApp:
    def __init__(self, chat_frame=None, users_frame=None, rooms_repo=None):
        self.chat_frame = chat_frame
        self.users_frame = users_frame
        self.rooms_repo = rooms_repo
        self.chat_screen = None
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        self.make_widgets()

    def make_widgets(self):
        self.chat_screen = ChatScreen(self.chat_frame, self.rooms_repo)

    def close(self):
        self.chat_screen.close()


if __name__ == "__main__":
    root = Tk()
    rooms = RoomRepository()
    root.geometry('600x400')
    root.configure(bg='beige')
    root.winfo_toplevel().title("FlowApp")

    # create all of the main containers
    top_frame = Frame(root, bg='gray', width=1024, height=60, pady=20)
    center = Frame(root, bg='gray2', width=1024, height=540, padx=3, pady=3)
    btm_frame = Frame(root, bg='gray', width=1024, height=60, pady=3)

    # layout all of the main containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")

    # create the widgets for the top frame
    model_label = Label(top_frame, text='Welcome to flow!', bg='gray')
    model_label.grid(row=0, columnspan=1)

    # create the center widgets
    center.grid_rowconfigure(0, weight=1)
    center.grid_columnconfigure(1, weight=1)

    ctr_mid = Frame(center, bg='white', width=824, height=540, padx=3, pady=3)
    ctr_right = Frame(center, bg='blue', width=0, height=540, padx=3, pady=3)

    ctr_mid.grid(row=0, column=1, sticky="nsew")
    ctr_right.grid(row=0, column=2, sticky="ns")

    app=FlowApp(ctr_mid, ctr_right, RoomRepository())

    root.mainloop()
    app.close()