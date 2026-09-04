import pip

modules = ('customtkinter', 'pillow', 'requests', 'CTkMessagebox', 'CTkToolTip')
for module in modules:
    pip.main(['install', module, '--upgrade'])