'''
Author : Sheikh_Rashdan
Version : 1.0.2
'''

# built-in modules
import socket, threading, os, random, subprocess

# pip installed modules
import customtkinter as ctk
from PIL import Image

# from files
from settings import *
from ui_tools import *


class Client(ctk.CTk):
    def __init__(self):
        super().__init__()

        # connection values
        self.HOST = None
        self.PORT = None
        self.USERNAME = None
        
        # display values
        self.images = self.load_images()
        self.address_var = ctk.StringVar(value = 'None')
        self.prev_msg_user = None
        self.prev_msg_label = None
        self.message_labels = []
        self.user_colors = {color:[] for color in UCOLORS}

        # lambda functions
        self.format_ip = lambda addr: f'{addr[0]}:{addr[1]}'

        # appearance
        self.title('ChitChat')
        self.iconbitmap('../assets/icons/client.ico')
        ctk.set_appearance_mode('dark')

        # geometry
        self.geometry(f'{CWIDTH}x{CHEIGHT}')
        self.resizable(False,False)

        # login
        self.login_page = create_frame(self, border_width = 0, fg_color = 'transparent', corner_radius = 0)
        self.login_page.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        self.login_page.columnconfigure(0, weight = 1, uniform = 'X')
        self.login_page.rowconfigure(0, weight = 5, uniform = 'X')
        self.login_page.rowconfigure((1,2,3,4), weight = 1, uniform = 'X')

        self.logo_label = create_label(self.login_page, image = self.images['logo'])
        self.logo_label.grid(column = 0, row = 0, sticky = 'news')

        self.username_entry = create_entry(self.login_page, placeholder_text = 'Username', justify = 'center', font_size = F[3], on_enter = lambda: self.address_entry.focus_set())
        self.username_entry.grid(column = 0, row = 1, sticky = 'news', padx = P2, pady = (2,4))

        self.address_entry = create_entry(self.login_page, placeholder_text = 'IP Address', justify = 'center', on_enter = lambda: self.connect_button._command())
        self.address_entry.grid(column = 0, row = 2, sticky = 'news', padx = P2, pady = 3)

        self.connect_button = create_button(self.login_page, text = 'Connect', font_size = F[3], command = self.check_connection_values)
        self.connect_button.grid(column = 0, row = 3, sticky = 'news', padx = P2, pady = (4,2))

        # chat
        self.chat_page = create_frame(self, border_width = 0, fg_color = 'transparent', corner_radius = 0)
        self.chat_page.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        self.chat_page.columnconfigure(0, weight = 1, uniform = 'X')
        self.chat_page.rowconfigure((0,2), weight = 1, uniform = 'X')
        self.chat_page.rowconfigure(1, weight = 8, uniform = 'X')

        self.chat_status_frame = create_frame(self.chat_page, border_width = 0, corner_radius = 0)
        self.chat_status_frame.grid(column = 0, row = 0, sticky = 'news')
        self.chat_status_label = create_label(self.chat_status_frame, textvariable = self.address_var, font = f'{FONT} Bold', cursor = 'hand2')
        self.chat_status_label.bind('<Button-1>', lambda e: self.copy_ip())
        create_tooltip(self.chat_status_label, message = 'Click to Copy IP')
        self.chat_status_label.pack(side = 'right', padx = P3)

        self.chat_disconnect_button = create_button(self.chat_status_frame, text = '⬅️', command = self.disconnect, width = 25)
        create_tooltip(self.chat_disconnect_button, message = 'Leave Room')
        self.chat_disconnect_button.pack(side = 'left', padx = P3)

        self.chat_display_frame = create_scrollable_frame(self.chat_page, corner_radius = 15)
        self.chat_display_frame.grid(column = 0, row = 1, sticky = 'news', padx = P3, pady = (P3,P1))

        self.chat_send_frame = create_frame(self.chat_page, border_width = 0, corner_radius = 0, fg_color = 'transparent')
        self.chat_send_frame.grid(column = 0, row = 2, sticky = 'news')
        self.chat_send_entry = create_entry(self.chat_send_frame, placeholder_text = 'Enter Message...', on_enter = lambda: self.chat_send_button._command())
        self.chat_send_entry.pack(side = 'left', expand = True, fill = 'both', padx = (P3,P1), pady = (0,P3))
        self.chat_file_button = create_button(self.chat_send_frame, text = '📁', width = 35, command = self.select_file)
        self.chat_file_button.pack(side = 'left', fill = 'both', padx = (0,P1), pady = (0,P3))
        self.chat_send_button = create_button(self.chat_send_frame, text = '🢁', width = 35, command = lambda: self.send_message(self.chat_send_entry.get()))
        create_tooltip(self.chat_send_button, message = 'Send Message')
        self.chat_send_button.pack(side = 'right', fill = 'both', padx = (0,P3), pady = (0,P3))

        # update
        self.login_page.lift()

        # exit protocol
        self.protocol('WM_DELETE_WINDOW', self.exit)

        # run
        self.mainloop()

    def load_images(self):
        '''
        Loads required images and returns them in the form of a dictionary.
        '''

        self.images = {}

        # logo
        logo = Image.open('../assets/logo/logo.png')
        logo = ctk.CTkImage(logo, size = (225,225))
        self.images['logo'] = logo

        return self.images

    def copy_ip(self):
        '''
        Copies the Public IP Address of the active connection to the clipboard.
        '''

        self.clipboard_clear()
        self.clipboard_append(self.address_var.get())

    def check_connection_values(self):
        '''
        Checks if all connection values are valid before attempting connection.
        '''

        self.USERNAME = self.username_entry.get()
        self.ADDRESS = self.address_entry.get()

        try:
            self.HOST = self.ADDRESS.split(':')[0]
            self.PORT = int(self.ADDRESS.split(':')[1])
            if not 0 <= self.PORT <= 65535:             # must be within 0 - 65535.
                raise ValueError
            else:
                if not self.USERNAME:                   # username must not be empty.
                    create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Invalid Username.')
                else:
                    for char in (' ', '\n', '\t'):
                        if char in self.USERNAME:       # username must not contain whitespaces.
                            create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Username Cannot Contain Space.')
                            break
                    else:
                        self.address_var.set(self.format_ip((self.HOST,self.PORT)))     # update connection address.
                        self.chat_send_entry.focus_set()                                # set focus to chat entry.
                        self.reset_display_values()                                     # reset display.

                        self.connection_thread = threading.Thread(target = self.connect)
                        self.connection_thread.daemon = True
                        self.connection_thread.start()
        except (IndexError,ValueError):         # ip address values incorrect.
            create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Invalid IP Address.')

    def reset_display_values(self):
        '''
        Resets chat display.
        '''

        for sub_widget in self.chat_display_frame.winfo_children():         # delete previous chats.
            sub_widget.destroy()
        self.message_labels.clear()                                         # clears stored messages.
        self.prev_msg_user = self.prev_msg_label = None                     # resets previous values.
        self.user_colors = {color:[] for color in UCOLORS}

    def connect(self):
        '''
        Attempts connection and sends username.
        '''

        connect = True

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.HOST,self.PORT))

            while True:
                password_status = self.client.recv(2048).decode()           # get password status.
                if password_status:                     # if password enabled
                    if 'enabled' in password_status:
                        response, password_var = create_entrybox(self, icon = 'info', title = 'Enter Password')         # input password.
                        confirmed = response.get()
                        if confirmed:           # if password entered
                            password = password_var.get()
                            self.client.send(password.encode())         # send password to server.
                            password_response = self.client.recv(2048).decode()         # get password status.
                            if '!conflict' in password_response:        # if password is incorrect.
                                create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Incorrect Password.')
                                connect = False
                        else:                   # if password not entered
                            connect = False
                    break
                
            if connect:
                self.client.send(f'!user {self.USERNAME}'.encode())         # sends username.
                username_response = self.client.recv(2048).decode()
                if '!conflict' in username_response:            # if username conflict occurs
                    self.disconnect(reason = '!conflict username')
                    create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Username Already Taken.')
                else:
                    self.listen()
            else:
                self.disconnect(reason = '!conflict password')

        except:         # connection failed.
            create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Connection Failed.')

    def disconnect(self, reason = '!disconnect'):
        '''
        Disconnects from the server and switches to login page.
        '''

        if reason == '!disconnect':            # if exiting connection
            self.client.send('!disconnect'.encode())
        elif '!conflict' in reason:      # if conflict occurs
            joinfail_reason = reason.split()[1]
            self.client.send(f'!joinfail {joinfail_reason}'.encode())
        self.client.close()         # closes connection.
        self.login_page.lift()      # switches to login page.

    def listen(self):
        '''
        Recieves responses from server and handles them.
        '''

        connected = True
        self.chat_page.lift()       # switches to chat page.

        try:
            while connected:
                response = self.client.recv(2048).decode()
                if response:
                    if response == '!stopping':         # if server is stopping
                        connected = False
                        create_messagebox(self, icon = 'info', title = 'Disconnected!', message = 'The Server Has Stopped.')
                    elif response == '!kicked':         # if server kicks client
                        connected = False
                        create_messagebox(self, icon = 'info', title = 'Disconnected!', message = 'You Have Been Kicked From The Server.')
                    elif '!msgreply' in response:       # if recieving a reply to a message
                        quote,username = response.split(' ')[1:3]
                        message = ' '.join(response.split(' ')[3:])
                        self.display_message(username, message, quote)
                    elif '!msg' in response:            # if recieving a message
                        username, _, message = response[5:].partition(' ')
                        self.display_message(username, message)
                    elif '!file' in response:           # if recieving a file
                        username, file_name = response[6:].split(' ')[:2]
                        file_name = file_name.replace('!space', ' ')
                        content = ' '.join(response.split(' ')[3:])
                        self.display_message(username, f'Sent File {file_name}')
                        self.display_file(username, file_name, content)
        except:
            pass        # connection closed abruptly.

        self.login_page.lift()          # swtiches to login page.
        self.client.close()             # closes connection.

    def send_message(self, message):
        '''
        Sends a chat message or chat reply message to the server.
        '''

        if message:         # if message is not empty
            if not self.prev_msg_label:         # if message is not reply
                self.client.send(f'!msg {self.USERNAME} {message}'.encode())
            else:                               # if message is reply
                quote = self.prev_msg_label._text.replace(' ', '!space')
                self.client.send(f'!msgreply {quote} {self.USERNAME} {message}'.encode())
                self.set_reply_message(self.prev_msg_label)
            self.chat_send_entry.delete(0, 'end')       # clears chat entry.

    def set_reply_message(self, message_label):
        '''
        Sets message to quote.
        '''

        if message_label != self.prev_msg_label:            # if message was not already selected
            for other_message_label in self.message_labels:
                other_message_label.configure(fg_color = 'transparent')
            message_label.configure(fg_color = BTNCLR2)
            self.prev_msg_label = message_label                  # select message
        else:                                               # if message was already selected
            message_label.configure(fg_color = 'transparent')
            self.prev_msg_label = None                           # deselect message

    def select_file(self):
        '''
        Selects file to send to the server.
        '''

        file = ctk.filedialog.askopenfile(filetypes = [('Text File','.txt')])           # returns file.
        try:
            file_name = file.name.split('/')[-1]              # get file name.
            with open(file.name, 'r') as f:
                content = f.read()          # get file conten.
            response = create_messagebox(self, icon = 'question', title = 'Confirm?', message = f'Send File {file_name}?', options = ['No', 'Yes'], button_width = 100)
            if response.get() == 'Yes':         # confirmation to send file.
                if content:         # if content exists
                    self.send_file(file_name, content)      # send file content.
                else:               # if content doesnt exist
                    create_messagebox(self, icon = 'warning', title = 'Error!', message = 'File Empty.')
        except:     # if file is invalid.
            create_messagebox(self, icon = 'warning', title = 'Error!', message = 'Failed To Send File.')

    def send_file(self, file_name, content):
        '''
        Sends file to the server.
        '''

        file_name = file_name.replace(' ', '!space')
        self.client.send(f'!file {self.USERNAME} {file_name} {content}'.encode())

    def display_message(self, username, message, quote = None):
        '''
        Displays message in chat.
        '''

        alignment = 'left'          # set alignment to left if sent by other
        if username == self.USERNAME:
            alignment = 'right'     # set alignment to the right if sent by self
            username = 'Me'         # set username to me if message sent by self
        
        # main frame
        content_frame = create_frame(self.chat_display_frame, border_width = 0, corner_radius = 0, fg_color = 'transparent')
        content_frame.pack(fill = 'x', padx = P1, pady = (P1,0))

        # if previous message was also sent by same username
        if username != self.prev_msg_user:

            # if user already assigned color
            for color, usernames in self.user_colors.items():
                if username in usernames:
                    user_color = color
                    break
            # if user not assigned color, select least used color
            else:
                minimum_users = len(self.user_colors[min(self.user_colors, key = lambda color: len(self.user_colors[color]))])
                available_colors = []
                for color, usernames in self.user_colors.items():
                    if len(usernames) == minimum_users:
                        available_colors.append(color)
                
                user_color = random.choice(available_colors)
                self.user_colors[user_color].append(username)
                
            username_frame = create_frame(content_frame, border_width = 0, fg_color = 'transparent', corner_radius = 0)
            username_frame.pack(fill = 'x')
            username_label = create_label(username_frame, text = username, font_size = F[0], wraplength = 100, text_color = user_color)
            username_label.pack(side = alignment)

        # if message is a reply
        if quote:
            quote = quote.replace('!space', ' ')
            quote_frame = create_frame(content_frame, border_width = 0, corner_radius = 0, fg_color = 'transparent')
            quote_frame.pack(fill = 'x')
            quote_label = create_label(quote_frame, text = quote, font_size = F[0], wraplength = 175, fg_color = CHAT_REPLY_CLR, justify = alignment)
            quote_label.pack(side = alignment, ipadx = P1)

        message_frame = create_frame(content_frame, border_width = 0, corner_radius = 0, fg_color = CHAT_FRAME_CLR)
        message_frame.pack(side = alignment)
        message_label = create_label(message_frame, text = message, wraplength = 175, justify = alignment)
        message_label.bind('<Button-1>', lambda e: self.set_reply_message(message_label))
        message_label.pack(ipadx = P3)

        # store message
        self.message_labels.append(message_label)

        # scroll down
        self.chat_display_frame._parent_canvas.yview('scroll', 50, 'pages')

        # set previous message username
        self.prev_msg_user = username

    def display_file(self, username, file_name, content):
        '''
        Stores file and display prompt to view file.
        '''

        if not os.path.exists("../files"): os.mkdir("../files")
        with open(f'../files/{file_name}', 'w') as f:
            f.write(content)
        
        alignment = 'left'              # set alignment to left if sent by other
        if username == self.USERNAME:
            alignment = 'right'         # set alignment to the right if sent by self

        file_frame = create_frame(self.chat_display_frame, border_width = 0, fg_color = 'transparent', corner_radius = 0)
        file_frame.pack(fill = 'x')
        file_button = create_button(file_frame, text = 'Open 📄', command = lambda: self.open_file(file_name))
        file_button.pack(side = alignment, padx = P3, pady = (P1,0))

    def open_file(self, file_name):
        '''
        View stored file.
        '''

        file_thread = threading.Thread(target = subprocess.run, args = (f'notepad "../files/{file_name}"',), kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW})
        file_thread.daemon = True
        file_thread.start()

    def exit(self):
        '''
        Closes connection before exiting the program.
        '''

        try:
            self.client.send('!disconnect'.encode())    # send message to server to disconnect.
            self.client.close()                         # closes connection.
        except:
            pass
        
        # closes program
        try:
            self.destroy()
        except:
            exit()


if __name__ == '__main__':
    Client()