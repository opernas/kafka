from tkinter import *
from DefaultRoomCreator import DefaultRoomCreator
from TextMessageEvent import TextMessageEvent
from NewFlowEvent import NewFlowEvent
from DefaultFlowCreator import DefaultFlowCreator
from GenericEvent import GenericEvent
from pydoc import locate


class ChatScreen:
    def __init__(self, main_frame=None, room_repo=None):
        self.room_repo = room_repo
        self.main_frame = main_frame
        self.listbox = None
        self.text_to_send = None
        self.join_window = None
        self.plugin_room_name = None
        self.buttons_frame = None
        self.chat_frame = None
        self.write_frame = None
        self.entry_room_name = None
        self.entry_num_messages = None
        self.chat_frame_listbox = None
        self.scrollbar = None
        self.closed = False
        self.accept_flow_window = None
        self.room_joined_name = None
        self.event_flow = None
        self.init_grid()
        self.create_chat_screen()
        self.create_write_frame()
        self.create_buttons()
        self.plugins_loaded={}

    def init_grid(self):
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.chat_frame = Frame(self.main_frame, bg='white', width=800, height=800, padx=3, pady=3)
        self.write_frame = Frame(self.main_frame, width=800, height=40, padx=3, pady=3)
        self.buttons_frame = Frame(self.main_frame, width=800, height=40, padx=3, pady=3)
        self.chat_frame.grid(row=1, sticky="nsew")
        self.write_frame.grid(row=2, sticky="sew")
        self.buttons_frame.grid(row=3, sticky="sew")

    def create_write_frame(self):
        self.write_frame.grid_columnconfigure(1, weight=1)
        write_frame_button = Frame(self.write_frame, width=800, height=40, padx=3, pady=3)
        write_frame_text = Frame(self.write_frame, width=800, height=40, padx=3, pady=3)
        self.text_to_send = Entry(self.write_frame, bd=5)
        self.text_to_send.grid(row=0, column=1, padx=7, pady=2, sticky="sew")
        Button(self.write_frame, text=' Send ', command=self.on_send_message).grid(row=0, column=0, padx=7, pady=2, sticky="nsew")

    def create_buttons(self):
        self.buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame1 = Frame(self.write_frame, width=800, height=40, padx=3, pady=3)
        buttons_frame2 = Frame(self.write_frame, width=800, height=40, padx=3, pady=3)
        Button(self.buttons_frame, text=' Join room ', command=self.on_wants_join).grid(row=3, column=0, padx=7, pady=2, sticky="nsew")
        Button(self.buttons_frame, text=' Add plugin ', command=self.on_wants_plugin).grid(row=3, column=1, padx=7, pady=2, sticky="nsew")

    def create_chat_screen(self):
        self.scrollbar = Scrollbar(self.chat_frame, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.chat_frame, width=600, height=600, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(expand=True, fill=Y)
        self.scrollbar.config(command=self.listbox.yview)

    def on_wants_plugin(self):
        print("Adding plugin in room ", self.room_joined_name)
        self.join_window = Tk()
        self.join_window.title('Adding plugin to room '+self.room_joined_name)
        frame = Frame(self.join_window)
        Label1 = Label(self.join_window, text='Plugin:')
        Label1.pack(padx=15, pady=5)
        self.plugin_room_name = Entry(self.join_window, bd=5)
        self.plugin_room_name.pack(padx=15, pady=5)
        btn = Button(frame, text=' Add plugin ', command=self.on_plugin_join)
        btn.pack(side=RIGHT, padx=5)
        frame.pack(padx=100, pady=19)
        x = self.main_frame.winfo_rootx()
        y = self.main_frame.winfo_rooty()
        self.join_window.geometry('%dx%d+%d+%d'%(400,150,x,y))
        self.join_window.mainloop()

    def on_plugin_join(self):
        self.import_user_plugin(self.plugin_room_name.get())

    def import_user_plugin(self, plugin_name):
        name = "userplugins."+plugin_name+"."+plugin_name
        room = self.room_repo.get(self.room_joined_name)
        user_plugin_class = locate(name)
        user_plugin_instance=user_plugin_class()
        user_plugin_instance.register(room)
        user_plugin_instance.start()
        self.plugins_loaded.update({plugin_name: user_plugin_instance})
        self.join_window.destroy()

    def on_send_message(self):
        if self.room_joined_name:
            print("sending message to room "+self.text_to_send.get())
            new_text_message = TextMessageEvent(self.text_to_send.get())
            room = self.room_repo.get(self.room_joined_name)
            room.send(new_text_message.serialize())

    def on_wants_join(self):
        print("joining room")
        self.join_window = Tk()
        self.join_window.title('Joining room')
        frame = Frame(self.join_window)
        Label1 = Label(self.join_window, text='Room:')
        Label1.pack(padx=15, pady=5)
        self.entry_room_name = Entry(self.join_window, bd=5)
        self.entry_room_name.pack(padx=15, pady=5)
        Label2 = Label(self.join_window, text='Num messages:')
        Label2.pack(padx=15, pady=5)
        self.entry_num_messages = Entry(self.join_window, bd=5)
        self.entry_num_messages.pack(padx=15, pady=5)
        btn = Button(frame, text=' Join ', command=self.on_join)
        btn.pack(side=RIGHT, padx=5)
        frame.pack(padx=100, pady=19)
        x = self.main_frame.winfo_rootx()
        y = self.main_frame.winfo_rooty()
        self.join_window.geometry('%dx%d+%d+%d'%(300,200,x,y))
        self.join_window.mainloop()

    def on_join(self):
        room = DefaultRoomCreator().create(self.entry_room_name.get(),
                                           self.entry_num_messages.get())
        self.room_joined_name = self.entry_room_name.get()
        self.room_repo.add(room)
        room.start(self.on_new_messages)
        self.join_window.destroy()

    def on_new_messages(self,data):
        if not self.closed:
            string_data = data.value.decode("utf-8")
            event = GenericEvent()
            event.deserialize(string_data)
            if event.get_type() == 'NewFlow':
                self.listbox.insert(END, string_data)
                self.request_user_accept_flow(string_data)
            else:
                self.listbox.insert(END, string_data)

    def request_user_accept_flow(self, string_data):
        print("accepting flow")
        self.event_flow = NewFlowEvent()
        self.event_flow.deserialize(string_data)
        self.accept_flow_window = Tk()
        self.accept_flow_window.title('Incoming flow on room '+self.room_joined_name)
        frame = Frame(self.accept_flow_window)
        label = Label(self.accept_flow_window, text=' Accept incoming flow with name: '+self.event_flow.get_body())
        label.pack(padx=15, pady=5)
        btn = Button(self.accept_flow_window, text=' Accept ', command=self.on_accept_flow)
        btn2 = Button(self.accept_flow_window, text=' Cancel ', command=self.on_not_accept_flow)
        btn.pack(side=RIGHT, padx=5)
        btn2.pack(side=RIGHT, padx=5)
        frame.pack(padx=10, pady=10)
        x = self.main_frame.winfo_rootx()
        y = self.main_frame.winfo_rooty()
        self.accept_flow_window.geometry('%dx%d+%d+%d'%(500,200,x,y))
        self.accept_flow_window.mainloop()

    def on_accept_flow(self):
        print("accepting flow", self.event_flow)
        self.accept_flow_window.destroy()
        room = self.room_repo.get(self.room_joined_name)
        flow_creator = DefaultFlowCreator()
        flow = flow_creator.create_flowing(self.event_flow.get_body(),
                                           self.event_flow.get_partition())
        room.accept_flow(flow, self.on_new_messages)

    def on_not_accept_flow(self):
        self.accept_flow_window.destroy()

    def close(self):
        self.closed = True
        self.room_repo.close()
        for name, plugin in self.plugins_loaded.items():
            plugin.stop()
        print("closing main...")

