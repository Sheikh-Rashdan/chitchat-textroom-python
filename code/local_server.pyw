'''
Author : Sheikh_Rashdan
Version : 1.0.2
'''


# built-in modules
import socket, threading

# pip-installed modules
import requests
import customtkinter as ctk

# from files
from settings import *
from ui_tools import *


class Server(ctk.CTk):
    def __init__(self):
        super().__init__()

        # control values
        self.server_active = False
        self.internet_connection = True

        # display values
        self.server_ip = None
        try:
            self.server_ip = socket.gethostbyname(socket.gethostname())         # returns public IPv4 address.
        except:
            self.internet_connection = False            # failed to get ip.

        # connection values
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.PASSWORD = None                    # password to join the connection
        self.connected_clients = {}             # active clients : username

        # commands
        self.commands = {'!help' : 'Displays all commands with their function.',
                         '!stop' : 'Disconnects all clients and stops the server.',
                         '!ip' : 'Copies The Server\'s IP Address To The Clipboard.',
                         '!password' : 'Copies The Servers\'s Password To The Clipboard.',
                         '!kick' : 'Kicks a specific user with their username or address.\n  syntax - !kick <ip:port> or !kick <username>',
                         '!connections' : 'Displays addresses and usernames of all active connections.',
                         '!clear' : 'Clears the console.',
                         '!sendmsg' : 'Send a message to all clients.\n  syntax - !sendmsg <message>',}

        # lambda functions
        self.format_ip = lambda addr: f'{addr[0]}:{addr[1]}'

        # appearance
        self.title('ChitChat Server')
        self.iconbitmap('../assets/icons/server.ico')
        ctk.set_appearance_mode('dark')

        # geometry
        self.geometry(f'{SWIDTH}x{SHEIGHT}')
        self.resizable(False,False)

        # main grid configuration
        self.columnconfigure(0, weight = 1, uniform = 'X')
        self.rowconfigure((0,3), weight = 1, uniform = 'X')
        self.rowconfigure(1, weight = 3, uniform = 'X')
        self.rowconfigure(2, weight = 3, uniform = 'X')

        # status frame
        self.status_frame = create_frame(self)
        self.status_frame.grid(column = 0, row = 0, sticky = 'news', padx = P1, pady = (P1,0))
        self.status_label = create_label(self.status_frame, text = f'Server Status : {"Online" if self.server_active else "Offline"} ⦿ ',
                                         text_color = ACTIVECLR if self.server_active else INACTIVECLR, font = f'{FONT} Italic')
        self.status_label.pack(expand = True)

        # control frame
        self.control_frame = create_frame(self)
        self.control_frame.grid(column = 0, row = 1, sticky = 'news', padx = P1, pady = P1)
        self.control_frame.columnconfigure((0,1), weight = 1, uniform = 'X')
        self.control_frame.rowconfigure((0,1,2), weight = 1, uniform = 'X')

        self.ip_label = create_label(self.control_frame, text = f'IP Address: {self.server_ip}', font_size = F[2], font = f'{FONT} Bold', cursor = 'hand2')
        self.ip_label.bind('<Button-1>', lambda e: self.copy_ip())
        self.ip_label.grid(column = 0, row = 0, columnspan = 2, sticky = 'news', padx = P1, pady = (P1,0))

        self.port_frame = create_frame(self.control_frame, border_width = 0, fg_color = 'transparent')
        self.port_frame.grid(column = 0, row = 1, sticky = 'news', padx = P1)
        self.port_label = create_label(self.port_frame, text = 'Port : ')
        self.port_label.pack(side = 'left', padx = (P1,0))
        self.port_entry = create_entry(self.port_frame, justify = 'center', def_value = 5050)
        self.port_entry.pack(side = 'right')

        self.password_frame = create_frame(self.control_frame, border_width = 0, fg_color = 'transparent')
        self.password_frame.grid(column = 0, row = 2, sticky = 'news', padx = P1, pady = (0,P1))
        self.password_label = create_label(self.password_frame, text = 'Password : ')
        self.password_label.pack(side = 'left', padx = (P1,0))
        self.password_entry = create_entry(self.password_frame, justify = 'center', placeholder_text = 'None', show = '•')
        self.password_entry.pack(side = 'right')

        self.button_frame = create_frame(self.control_frame)
        self.button_frame.grid(column = 1, row = 1, rowspan = 2, sticky = 'news', padx = P1, pady = P1)
        self.start_button = create_button(self.button_frame, text = 'Start', state = 'disabled' if self.server_active else 'normal', command = self.check_server_values)
        self.start_button.pack(expand = True, fill = 'both', padx = 2, pady = 2)
        self.stop_button = create_button(self.button_frame, text = 'Stop', state = 'normal' if self.server_active else 'disabled', command = self.toggle_server_state)
        self.stop_button.pack(expand = True, fill = 'both', padx = 2, pady = 2)

        # log frame
        self.log_textbox = create_textbox(self, state = 'disabled')
        self.log_textbox.grid(column = 0, row = 2, sticky = 'news', padx = P1, pady = (0,P1))
        self.log_textbox.tag_config('Error', foreground = 'red')
        self.log_textbox.tag_config('Command', foreground = 'yellow')
        self.log_textbox.tag_config('Connection', foreground = 'green')

        # command frame
        self.command_frame = create_frame(self)
        self.command_frame.grid(column = 0, row = 3, sticky = 'news', padx = P1, pady = (0,P1))
        self.command_frame.columnconfigure(0, weight = 7, uniform = 'X')
        self.command_frame.columnconfigure(1, weight = 1, uniform = 'X')
        self.command_frame.rowconfigure(0, weight = 1, uniform = 'X')

        self.command_entry = create_entry(self.command_frame, placeholder_text = 'Enter Command...', state = 'disabled', on_enter = lambda: self.command_button._command())
        self.command_entry.grid(column = 0, row = 0, sticky = 'news', padx = P1, pady = P1)
        self.command_button = create_button(self.command_frame, text = '🢁', command = lambda: self.execute(self.command_entry.get()))
        self.command_button.grid(column = 1, row = 0, sticky = 'news', padx = (0,P1), pady = P1)

        # exit protocol
        self.protocol('WM_DELETE_WINDOW', self.exit)

        # run
        self.mainloop()

    def log(self, _from, message, tags = None):
        '''
        Logs message from a particular source to the logbox with color tags.
        '''

        if _from == 'Error':
            tags = 'Error'
        if _from == '>>':
            tags = 'Command'
        self.log_textbox.configure(state = 'normal')
        self.log_textbox.insert('end', f'[{_from}] {message}\n', tags = tags)
        self.log_textbox.configure(state = 'disabled')
        self.log_textbox.yview_scroll(1, 'units')

    def copy_ip(self):
        '''
        Copies the Public IP Address of the server to the clipboard.
        '''
        ip_address = f'{self.server_ip}:{self.PORT}'
        self.clipboard_clear()
        self.clipboard_append(ip_address)
        self.log('Server', f'Copied IP Address To Clipboard.\nIP : {ip_address}')

    def copy_password(self):
        '''
        Copies the Password of the server to the clipboard.
        '''
        password = self.PASSWORD if self.PASSWORD else 'None'
        self.clipboard_clear()
        self.clipboard_append(password)
        self.log('Server', f'Copied IP Address To Clipboard.\nPASSWORD : {password}')

    def check_server_values(self):
        '''
        Checks if the entered server values are correct and starts the server.
        '''

        check = False

        try:
            self.PASSWORD = self.password_entry.get()
            self.PORT = int(self.port_entry.get())          # must be numeric.
            if not 0 <= self.PORT <= 65535:                 # must be within 0 - 65535.
                self.log('Error', 'Invalid Value - Port must be within 0 - 65535.')
            else:
                check = True
        except ValueError:
            self.log('Error', 'Invalid Value - Port must be numeric.')

        if check:
            self.toggle_server_state()

    def toggle_server_state(self):
        '''
        Toggles the server state between inactive and active.
        '''

        # toggles values
        self.server_active = not self.server_active
        self.status_label.configure(text = f'Server Status : {"Online" if self.server_active else "Offline"} ⦿ ',
                                    text_color = ACTIVECLR if self.server_active else INACTIVECLR)
        self.port_entry.configure(state = 'disabled' if self.server_active else 'normal')
        self.password_entry.configure(state = 'disabled' if self.server_active else 'normal')
        self.start_button.configure(state = 'disabled' if self.server_active else 'normal')
        self.stop_button.configure(state = 'normal' if self.server_active else 'disabled')
        self.command_entry.delete(0, 'end')
        self.command_entry.configure(state = 'normal' if self.server_active else 'disabled')

        if self.server_active:          # starts server
            self.connection_thread = threading.Thread(target = self.activate_server)
            self.connection_thread.daemon = True
            self.connection_thread.start()
        else:                           # stops server  
            self.log('Server', 'Disconnecting All Clients.')
            try:
                for client in self.connected_clients:           # closes all connections
                    self.send_message(client, '!stopping')
                    client.close()
            except:
                pass
            self.server.close()

        self.log('Server', 'Server Starting...' if self.server_active else 'Server Stopped.')

    def activate_server(self):
        '''
        Turns the server on.
        '''

        # creates server 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST,self.PORT))
        self.server.listen()
        self.log('Server', f'Server Started At {self.format_ip((self.HOST,self.PORT))}.')
        
        # checks for connections
        while self.server_active:
            try:
                client, addr = self.server.accept()
                self.log('Server', f'Client Connected From {self.format_ip(addr)}', tags = 'Connection')
                threading.Thread(target = self.handle_client, args = (client,addr)).start()
            except OSError:
                break

    def handle_client(self, client: socket.socket, addr):
        '''
        Recieves responses from client connection and handles them.
        '''

        connected = True
        self.connected_clients[client] = None       # set username to None
        
        try:
            
            if self.PASSWORD:                                           # if password enabled
                self.send_message(client, '!password enabled')              # inform client about password status.
                password_response = client.recv(2048).decode()              # get password from client.
                if password_response != self.PASSWORD:                      # if password incorrect
                    self.send_message(client, '!conflict pasword')          # inform client about password status.
                else:
                    self.send_message(client, '!accept password')           # inform client about password status.
            else:                                                       # if password not enabled
                self.send_message(client, '!password disabled')             # inform client about password status.

            while connected:
                response = client.recv(2048).decode()
                if response:
                    if response == '!disconnect':           # user disconnecting.
                        connected = False
                        self.log('Server', f'{username} Disconnected.', tags = 'Connection')
                        self.send_message_to_all(f'!msg Server {username} Left.')
                    elif '!joinfail' in response:           # user failed to join.
                        connected = False
                        reason = response.split()[1]            # get joinfail reason.
                        if reason == 'username':
                            self.log('Server', f'{addr} Failed To Join Due To Conflicting Username.')
                        elif reason == 'password':
                            self.log('Server', f'{addr} Failed To Join Due To Incorrect Password.')
                    elif '!user' in response:               # user sending username.
                        username = response.split()[1]
                        if username and username not in self.connected_clients.values():        # if username valid
                            self.connected_clients[client] = username
                            self.send_message(client, '!accept username')
                            self.log('Server', f'Registered {self.format_ip(addr)} As {username}.')
                            self.send_message_to_all(f'!msg Server {username} Joined.')
                        else:                                                                   # if username invalid
                            self.send_message(client, '!conflict username')
                    elif '!msg' in response or '!file' in response:         # user sending message or file.
                        self.send_message_to_all(response)
                    else:                                               # user sending invalid response.
                        self.log(username, response)
        except:
            pass        # connection closed abruptly.
        
        # close
        client.close()
        if client in self.connected_clients:
            del self.connected_clients[client]          # remove client from connected clients.

    def send_message_to_all(self, message):
        '''
        Sends a message to all connected clients.
        '''

        for client in self.connected_clients:
            self.send_message(client, message)

    def send_message(self, client, message):
        '''
        Sends a message to a particular client
        '''

        client.send(message.encode())

    def execute(self, command):
        '''
        Execute a server command.
        '''

        try:
            if command:             # if command is not empty
                self.log('>>', command)
                self.command_entry.delete(0, 'end')         # clear command entry.
                if not command[0] == '!':                   # if command does not contain "!"
                    self.log('Error', 'Invalid Command - All Commands Must Begin With "!".')
                else:
                    command_words = command.split()         # get command parameters.
                    command_key = command_words[0]          # main command function.
                    if not command_key in self.commands:            # if command not in list of commands
                        self.log('Error', 'Invalid Command - Command Not Recognised.')
                    else:

                        match command_key:
                            case '!help':
                                commands = '\n'.join([f'{command}: {description}' for command,description in self.commands.items()])
                                self.log('Server', f'The Available Commands Are -\n{commands}')

                            case '!stop':
                                self.toggle_server_state()

                            case '!ip':
                                self.copy_ip()

                            case '!password':
                                self.copy_password()

                            case '!kick':
                                user = command_words[1]
                                for client in self.connected_clients:
                                    client_ip = self.format_ip(client.getpeername())
                                    if client_ip == user or self.connected_clients[client] == user:
                                        username = self.connected_clients[client] if self.connected_clients[client] else 'Unregistered'
                                        self.send_message(client, '!kicked')
                                        self.send_message_to_all(f'!msg Server Kicked "{username}".')
                                        self.log('Server', f'Kicked User "{username}" From {client_ip}.', tags = 'Connection')
                                        client.close()
                                        del self.connected_clients[client]
                                        break
                                else:
                                    self.log('Error', f'Invalid Syntax - "{user}" Not Recognised.')
                                    
                            case '!connections':
                                if self.connected_clients:
                                    for client in self.connected_clients:
                                        self.log('Server', f'{client.getpeername()} - {self.connected_clients[client]}')
                                else:
                                    self.log('Server', 'No Active Connections.')

                            case '!clear':
                                self.log_textbox.configure(state = 'normal')
                                self.log_textbox.delete('0.0','end')
                                self.log_textbox.configure(state = 'disabled')

                            case '!sendmsg':
                                message = ' '.join(command_words[1:])
                                self.send_message_to_all(f'!msg Server {message}')
                                self.log('Server', 'Sent Message To All Clients.')

                            case _:         # if command in command list but not implemented
                                self.log('Server', 'Command Not Implemented.')

        except IndexError:          # command parameter missing.
            self.log('Error', 'Invalid Command Parameter.')

    def exit(self):
        '''
        Closes all connections before exiting the program.
        '''

        try:
            for client in self.connected_clients:       # closes all connections.
                self.send_message(client, '!stopping')
                client.close()
            self.server.close()                         # closes server.
        except:
            pass

        self.destroy()          # closes program.


if __name__ == '__main__':
    Server()