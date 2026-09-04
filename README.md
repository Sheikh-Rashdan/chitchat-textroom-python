# ChitChat

ChitChat is a small desktop chat application built with Python, CustomTkinter, and TCP sockets. It supports multiple clients in one chat room, optional server passwords, message replies, file sharing, and server-side connection management.

## Features

- Dark-themed graphical client and server interfaces
- Multiple clients connected to one server
- Optional password-protected rooms
- Usernames with duplicate-name protection
- Message replies and shared text files
- Server commands for monitoring and moderation
- Local-network and internet server launchers

## Gallery

<p align="center">
  Server <br />
  <img width="563" height="538" alt="chitchat-server" src="https://github.com/user-attachments/assets/a495de7e-9d0e-43ca-8008-99344eaff5cc" /><br /><br />
  Client <br />
  <img width="377" height="601" alt="chitchat-client-connection" src="https://github.com/user-attachments/assets/4f343c0f-d1b9-4a73-9d1e-2e641af7e689" /><br /><br />
  <img width="377" height="601" alt="chitchat-client-chatroom" src="https://github.com/user-attachments/assets/a0e0595b-19b7-43ab-906b-05ef502db0ae" /><br /><br />
</p>

## Requirements

- Windows, macOS, or Linux with Python 3
- A network connection when chatting between different machines

The client and server use these third-party packages:

- `customtkinter`
- `Pillow`
- `requests`
- `CTkMessagebox`
- `CTkToolTip`

## Installation

From the project root, install the dependencies with:

```text
python install_modules.py
```

You can also install them manually with:

```text
python -m pip install --upgrade customtkinter pillow requests CTkMessagebox CTkToolTip
```

### Optional: Install the bundled fonts

ChitChat uses `Source Code Pro` and `Staatliches` for its interface. The font files are included in `assets/fonts`. On Windows, right-click each `.ttf` file and select **Install** or **Install for all users**. The application will still run without installing them, but the interface may use fallback fonts.

## Running ChitChat

The launcher files use paths relative to the `code` directory. Open a terminal in that directory before starting the application:

```text
cd code
```

### Start a server

For a server intended for internet connections, run:

```text
python server.pyw
```

For a server intended for clients on the same local network, run:

```text
python local_server.pyw
```

The default port is `5050`. The server window allows you to change the port and optionally set a password before selecting **Start**. Share the displayed address and port with clients. Windows Firewall or router port forwarding may need to be configured for connections from outside the local network.

### Start a client

```text
python client.pyw
```

Enter a username and the server address in the form `IP_ADDRESS:PORT`, for example:

```text
192.168.1.20:5050
```

## Server Commands

Enter commands in the server window while the server is running:

| Command                         | Description                                 |
| ------------------------------- | ------------------------------------------- |
| `!help`                       | Display the available commands.             |
| `!stop`                       | Disconnect all clients and stop the server. |
| `!ip`                         | Copy the server address to the clipboard.   |
| `!password`                   | Copy the server password to the clipboard.  |
| `!kick <username or ip:port>` | Disconnect a specific client.               |
| `!connections`                | Display connected clients.                  |
| `!clear`                      | Clear the server log.                       |
| `!sendmsg <message>`          | Send a message to all clients.              |

## Project Structure

```text
ChitChat/
├── assets/              # Icons, logo, and fonts
├── code/
│   ├── client.pyw       # Chat client
│   ├── local_server.pyw # Local-network server
│   ├── server.pyw       # Internet-oriented server
│   ├── settings.py      # Shared UI settings
│   └── ui_tools.py      # Shared CustomTkinter helpers
├── install_modules.py   # Dependency installer
└── !commands.txt       # Protocol and command reference
```

## Notes

- The server listens on TCP port `5050` by default.
- Clients and servers must be able to reach one another on the selected address and port.
- Keep the server window open while clients are connected.
- Only share a server password with people who should be able to join the room.
