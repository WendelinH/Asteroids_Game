import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--name=Assteroids_Game",
    "--windowed",
    "--icon=./image/icon.ico",
    "--add-data=./image:image",
    "--add-data=./fonts:fonts"
])