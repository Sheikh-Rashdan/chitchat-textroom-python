import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip
from settings import *

def create_frame(parent, *, border_width = FRAME_BW, border_color = FRAME_BC, **kwargs):

    frame = ctk.CTkFrame(parent,
                         border_width = border_width,
                         border_color = border_color,
                         **kwargs)
    
    return frame

def create_textbox(parent, *, border_width = FRAME_BW, border_color = FRAME_BC, font = FONT, font_size = F[0], **kwargs):

    textbox = ctk.CTkTextbox(parent,
                             border_width = border_width,
                             border_color = border_color,
                             font = (font,font_size),
                             wrap = 'word',
                             **kwargs)

    return textbox

def create_label(parent, *, text = '', image = None, text_color = TEXTCLR, font = FONT, font_size = F[1], **kwargs):

    label = ctk.CTkLabel(parent,
                         text = text,
                         image = image,
                         text_color = text_color,
                         font = (font,font_size),
                         **kwargs)
    
    return label

def create_entry(parent, *, placeholder_text = '', text_color = TEXTCLR, font = FONT, font_size = F[1], def_value = None, on_enter = None, **kwargs):

    entry = ctk.CTkEntry(parent,
                         placeholder_text = placeholder_text,
                         text_color = text_color,
                         font = (font,font_size),
                         **kwargs)
    
    if on_enter:
        entry.bind('<Return>', lambda e: on_enter())
    
    if def_value:
        entry.insert(0, str(def_value))

    return entry

def create_button(parent, *, text, text_color = TEXTCLR, font = FONT, font_size = F[1], fg_color = BTNCLR1,
                  border_color = BTNCLR2, hover_color = BTNCLR2, border_width = 2, command = None, **kwargs):

    button = ctk.CTkButton(parent,
                           text = text,
                           text_color = text_color,
                           font = (font,font_size),
                           fg_color = fg_color,
                           border_color = border_color,
                           hover_color = hover_color,
                           border_width = border_width,
                           command = command,
                           **kwargs)
    
    return button

def create_messagebox(parent, *, icon, title, message, **kwargs):

    message = CTkMessagebox(parent,
                            width = 300,
                            icon = icon,
                            title = title,
                            message = message,
                            options = kwargs.get('options'),
                            button_width = kwargs.get('button_width'),
                            button_color = BTNCLR1,
                            button_hover_color = BTNCLR2,
                            title_color = TEXTCLR,
                            text_color = TEXTCLR,
                            button_text_color = TEXTCLR,
                            font = ('Staatliches',F[2]),
                            sound = True)
     
    return message

def create_entrybox(parent, *, icon, title, **kwargs):

    entrybox = create_messagebox(parent, icon = icon, title = title, message = ' '*100, **kwargs)

    entry_var = ctk.StringVar()
    entry = create_entry(entrybox, on_enter = lambda: entrybox.button_1._command())
    entry.configure(textvariable = entry_var, bg_color = ('#cfcfcf','#333333'))
    entry.place(relx = 0.6, rely = 0.475, anchor = 'center')

    return entrybox, entry_var

def create_tooltip(parent, *, message, delay = 0.1):

    tool = CTkToolTip(parent,
                      message = message,
                      delay = delay,
                      x_offset = 10,
                      bg_color = TEXTCLR,
                      text_color = BTNCLR1,
                      font = (f'{FONT} Black', F[0]),
                      border_width = 1,
                      corner_radius = 5,
                      padding = (6,0))
    
    return tool

def create_scrollable_frame(parent, *, border_width = FRAME_BW, border_color = FRAME_BC, **kwargs):

    frame = ctk.CTkScrollableFrame(parent,
                                   border_width = border_width,
                                   border_color = border_color,
                                   **kwargs)

    return frame
