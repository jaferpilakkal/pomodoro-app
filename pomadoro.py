from tkinter import ttk
from tkinter import *
import math
import os, sys
from playsound import playsound
from tkinter import messagebox
import random
import json


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#f57c00"
RED = "#c62828"
GREEN = "#388e3c"
YELLOW = "#f1f8e9"
BUTTON_GREEN = "#b9fbc0"

FONT_NAME = "Courier"

# Default durations
DEFAULT_WORK_MIN = 25
DEFAULT_SHORT_BREAK_MIN = 5
DEFAULT_LONG_BREAK_MIN = 15

# Mutable durations
WORK_MIN = DEFAULT_WORK_MIN
SHORT_BREAK_MIN = DEFAULT_SHORT_BREAK_MIN
LONG_BREAK_MIN = DEFAULT_LONG_BREAK_MIN

CONFIG_FILE = "settings.json"

sound_enabled = True
bring_to_front_enabled = True

reps = 0
timer = None
already_started = False
is_paused = False
paused_time = 0
sets_completed = 0
work_sessions = 0
current_session_total = 0


#-------add hover color effect on buttons-----------
def on_enter(e):
    current_bg = e.widget.original_bg
    if current_bg == BUTTON_GREEN:
        e.widget['background'] = "#a2e6ae"  # darker green
    elif current_bg == PINK:
        e.widget['background'] = "#dc6a00"  # darker orange
    elif current_bg == RED:
        e.widget['background'] = "#b71c1c"  # darker red
    elif current_bg == "white":
        e.widget['background'] = "#dce3c4"
def on_leave(e):
    e.widget['background'] = e.widget.original_bg


#----------------function to find file path when bundles with pyinstaller--------
def resource_path(filename):
    """ Get path to the bundled file """
    if getattr(sys, '_MEIPASS', False):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath('.'), filename)

# -------------function to restore settings------------

def load_user_settings():
    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, sound_enabled, bring_to_front_enabled

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                settings = json.load(f)
                WORK_MIN = settings.get("work", DEFAULT_WORK_MIN)
                SHORT_BREAK_MIN = settings.get("short_break", DEFAULT_SHORT_BREAK_MIN)
                LONG_BREAK_MIN = settings.get("long_break", DEFAULT_LONG_BREAK_MIN)
                sound_enabled = settings.get("sound_enabled", True)
                bring_to_front_enabled = settings.get("bring_to_front_enabled", True)
        except Exception:
            pass  # If error reading file, just fall back to defaults



#----------random quotes under title-----------------


WORK_QUOTES = [
    "Don't look at me. Focus on your work.",
    "Time to grind — no distractions.",
    "Deep work mode: activated.",
    "Heads down. You’ve got stuff to do.",
    "Now is not the time to scroll. Focus.",
    "Work time. Get something done!",
    "Laser focus, no excuses.",
    "Just 25 minutes. Give it your best shot.",
    "Get in, get it done, get out.",
    "This is your productivity window. Use it.",
    "Let’s build momentum. Start working.",
    "Clear your mind. Stay in the zone.",
    "One task. One goal. Let’s go.",
    "You're capable. Prove it now.",
    "Shut the world out. It's work time.",
    "Respect the timer. Focus now.",
    "You wanted progress? Start typing.",
    "Make it count. Every second matters.",
    "Working now means relaxing later.",
    "Pomodoro says: Work. No debates."
]
BREAK_QUOTES = [
    "Break time! Get up and move.",
    "You earned this — take a short break.",
    "Relax. Breathe. Reset.",
    "Stretch your legs, clear your mind.",
    "Step away for a bit, then come back stronger.",
    "Break time: water, walk, rest.",
    "Time to pause. You've done well.",
    "Rest your brain. It deserves it.",
    "Take a moment. Don’t check emails.",
    "Enjoy this pause — no guilt.",
    "Move your body, refresh your mind.",
    "Break = productivity fuel. Use it well.",
    "Look away from the screen. Yes, now.",
    "Time to chill. Just a little.",
    "Short rest before the next sprint.",
    "You've been awesome. Now breathe.",
    "Let your brain idle. It's part of the process.",
    "Hydrate. Smile. Stretch.",
    "This pause is power. Don’t skip it.",
    "No multitasking. Just enjoy the break."
]

MOTIVATION_QUOTES = [
    "Small steps every day lead to big results.",
    "Discipline beats motivation.",
    "Stay consistent. Even when it's boring.",
    "Success is built one session at a time.",
    "Progress, not perfection.",
    "You're building something. Keep going.",
    "What you do now adds up later.",
    "Focus is your superpower.",
    "Don’t break the chain.",
    "Future you will thank you for this.",
    "One Pomodoro at a time. That’s the secret.",
    "You’re showing up — and that matters.",
    "Consistency creates confidence.",
    "Time is your most valuable asset. Use it well.",
    "No zero days. Do something small.",
    "Build momentum. Don’t wait for motivation.",
    "Your goals need your time — not just your dreams.",
    "Every focused minute is a vote for your future.",
    "This session is one brick in your empire.",
    "Hard now, easy later. Let’s go!"
]
RESUME_QUOTES = [
    "Welcome back. Let's finish what you started. ",
    "You paused, but you didn’t quit. Let’s go. ",
    "Picking it back up — that’s what matters. ",
    "Distractions happen. Focus wins. ",
    "Progress isn’t perfect — just consistent. ",
    "You’re back. That’s what counts. ",
    "Momentum regained is a power move. ",
    "Restarting is still winning. ",
    "Breaks are fine. Getting back is growth. ",
    "Focus mode: resumed. Let’s crush it. "
]


def get_random_work_quote():
    return random.choice(WORK_QUOTES)
def get_random_break_quote():
    return random.choice(BREAK_QUOTES)
def get_random_motivation_quote():
    return random.choice(MOTIVATION_QUOTES)
def get_resume_quote():
    return random.choice(RESUME_QUOTES)

#----------Save Settings function----------------
def save_user_settings():
    settings = {
        "work": WORK_MIN,
        "short_break": SHORT_BREAK_MIN,
        "long_break": LONG_BREAK_MIN,
        "sound_enabled": sound_enabled,
        "bring_to_front_enabled": bring_to_front_enabled
    }
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f)
    except Exception:
        pass




# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global already_started, reps, is_paused, work_sessions,sets_completed
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text = "00:00")
    title_label.config(text ="Let's Pomodoro!", fg = GREEN)
    checkmark_label.config(text = " ")
    reps = 0
    work_sessions = 0
    sets_completed = 0
    already_started = False
    is_paused = False
    start_button.config(text="Start", bg = BUTTON_GREEN, fg= "black")
    start_button.original_bg = BUTTON_GREEN
    reset_button.config(bg = BUTTON_GREEN, fg = "black")
    reset_button.original_bg = BUTTON_GREEN
    pomodoro_set_label.config(text=f"Pomodoro Sets: {sets_completed}")
    progress_canvas.coords(progress_fill, 0, 0, 0, 20)
    progress_canvas.itemconfig(progress_text, text="0%")
    progress_canvas.itemconfig(progress_fill, fill=GREEN)


def show_summary():
    messagebox.showinfo(title="Session Summary", message=f"Congratulations!\nYou completed {sets_completed} Pomodoro Sets\n({work_sessions} work sessions)!")

def change_session(session):
    if session == "short_break":
        title_label.config(text="It's Break Time!", fg=PINK)
        quote_label.config(text=get_random_break_quote())
        start_button.config(bg=PINK, fg="white")
        reset_button.config(bg=PINK, fg="white")
        start_button.original_bg = PINK
        reset_button.original_bg = PINK
        #progress bar bg color
        progress_canvas.itemconfig(progress_fill, fill= PINK)



    elif session == "long_break":
        title_label.config(text="It's Break Time!", fg=RED)
        quote_label.config(text=get_random_break_quote())
        start_button.config(bg=RED, fg="white")
        reset_button.config(bg=RED, fg="white")
        start_button.original_bg = RED
        reset_button.original_bg = RED
        #progress bar bg color
        progress_canvas.itemconfig(progress_fill, fill= RED)



    elif session == "work":
        title_label.config(text="It's Focus Time!", fg=GREEN)
        quote_label.config(text=get_random_work_quote())
        start_button.config(bg=BUTTON_GREEN, fg="black")
        reset_button.config(bg=BUTTON_GREEN, fg="black")
        start_button.original_bg = BUTTON_GREEN
        reset_button.original_bg = BUTTON_GREEN

        progress_canvas.itemconfig(progress_fill, fill= GREEN)


    elif session == "pause":
        start_button.config(text="Resume", bg=BUTTON_GREEN, fg="black")
        reset_button.config(bg=BUTTON_GREEN, fg="black")
        title_label.config(text="Get Back on Track!", fg=GREEN)
        quote_label.config(text=get_resume_quote())
        start_button.original_bg = BUTTON_GREEN
        reset_button.original_bg = BUTTON_GREEN

        progress_canvas.itemconfig(progress_fill, fill= GREEN)


#------------bring window to front---------------------
def bring_window_to_front():
    if bring_to_front_enabled:
        window.deiconify()  # Restore if minimized
        window.lift()
        window.attributes('-topmost', True)
        window.after(1000, lambda: window.attributes('-topmost', False))

# ----------------------------  ----------SESSION START--------------------- #

def start_new_session():
    global reps, current_session_total

    bring_window_to_front()

    reps += 1

    if (reps - 1) % 8 == 0:
        checkmark_label.config(text="")  # Reset checkmarks at start of second cycle

    work_sec = int(WORK_MIN) * 60
    short_break_sec = int(SHORT_BREAK_MIN) * 60
    long_break_sec = int(LONG_BREAK_MIN) * 60


    if reps % 8 == 0:
        count = long_break_sec
        current_session_total = count
        change_session("long_break")

    elif reps % 2 == 0:
        count = short_break_sec
        current_session_total = count
        change_session("short_break")

    else:
        count = work_sec
        current_session_total = count
        change_session("work")

    count_down(count)

#---------------Settings mechanism--------------------------

def open_settings():
    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, sound_enabled

    def apply_settings():
        nonlocal work_entry, short_entry, long_entry, sound_var

        try:
            new_work = float(work_entry.get())
            new_short = float(short_entry.get())
            new_long = float(long_entry.get())

            if new_work <= 0 or new_short <= 0 or new_long <= 0:
                raise ValueError("Durations must be positive.")

            # Update durations
            globals()['WORK_MIN'] = new_work
            globals()['SHORT_BREAK_MIN'] = new_short
            globals()['LONG_BREAK_MIN'] = new_long
            globals()['sound_enabled'] = sound_var.get()
            globals()['bring_to_front_enabled'] = bring_to_front_var.get()

            save_user_settings()

            if messagebox.askyesno("Apply Settings", "Applying settings will reset the current session. Continue?"):
                reset_timer()
                messagebox.showinfo("Settings Saved", "Settings applied and timer reset.")
                settings_window.destroy()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def reset_to_defaults():
        work_entry.delete(0, END)
        short_entry.delete(0, END)
        long_entry.delete(0, END)

        work_entry.insert(0, DEFAULT_WORK_MIN)
        short_entry.insert(0, DEFAULT_SHORT_BREAK_MIN)
        long_entry.insert(0, DEFAULT_LONG_BREAK_MIN)

        bring_to_front_var.set(True)
        sound_var.set(True)

    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("420x430")
    settings_window.resizable(False, False)
    settings_window.config(bg=YELLOW)

    settings_window.lift()
    settings_window.attributes('-topmost', True)
    settings_window.after(500, lambda: settings_window.attributes('-topmost', False))

    Label(settings_window, text="About", font=(FONT_NAME, 12, "bold"), bg=YELLOW).pack(pady=(10, 0))
    Label(settings_window, text="Pomodoro App by Jafar Swadique\njaferpilakkal@gmail.com\nVersion 1.0", bg=YELLOW).pack()

    Label(settings_window, text="How it works", font=(FONT_NAME, 12, "bold"), bg=YELLOW).pack(pady=(15, 0))
    Label(settings_window, text="Work → Break → Repeat\n4 cycles = Long Break", bg=YELLOW).pack()

    Label(settings_window, text="Customize Durations (minutes)", font=(FONT_NAME, 12, "bold"), bg=YELLOW).pack(pady=(20, 0))

    form_frame = Frame(settings_window, bg=YELLOW)
    form_frame.pack(pady=5)

    Label(form_frame, text="Work:", bg=YELLOW).grid(row=0, column=0, sticky="e")
    work_entry = Entry(form_frame, width=5)
    work_entry.grid(row=0, column=1)
    work_entry.insert(0, WORK_MIN)

    Label(form_frame, text="Short Break:", bg=YELLOW).grid(row=1, column=0, sticky="e")
    short_entry = Entry(form_frame, width=5)
    short_entry.grid(row=1, column=1)
    short_entry.insert(0, SHORT_BREAK_MIN)

    Label(form_frame, text="Long Break:", bg=YELLOW).grid(row=2, column=0, sticky="e")
    long_entry = Entry(form_frame, width=5)
    long_entry.grid(row=2, column=1)
    long_entry.insert(0, LONG_BREAK_MIN)

    sound_var = BooleanVar(value=sound_enabled)
    Checkbutton(settings_window, text="Enable Sound", variable=sound_var, bg=YELLOW).pack(pady=5)

    bring_to_front_var = BooleanVar(value=bring_to_front_enabled)
    Checkbutton(settings_window, text="Bring Window to Front on Session Start", variable=bring_to_front_var,
                bg=YELLOW).pack(pady=5)

    Button(settings_window, text="Save & Close", command=apply_settings, bg=BUTTON_GREEN).pack(pady=5)
    Button(settings_window, text="Reset to Defaults", command=reset_to_defaults, bg=RED, fg="white").pack(pady=5)



# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global already_started, is_paused,paused_time
    if not already_started:
        already_started = True
        is_paused = False
        start_new_session()
    else:
        if is_paused:
            # Resume
            is_paused = False
            count_down(paused_time)
            start_button.config(text="Pause")
            if reps % 8 == 0:
                change_session("long_break")
            elif reps  % 2 == 0:
                change_session("short_break")
            else:
                change_session("work")

        else:
            # Pause
            is_paused = True
            window.after_cancel(timer)
            change_session("pause")

def play_sound():
    if sound_enabled:
        try:
            sound_file = resource_path("alarm.mp3")  # Make sure it's included when packaging
            playsound(sound_file)
        except Exception:
            pass
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, paused_time, reps, sets_completed, work_sessions, current_session_total

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count:  # only on first call after start/resume
        start_button.config(text="Pause")

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text,text = f"{count_min}:{count_sec}")

    if current_session_total > 0:
        completed = (current_session_total - count) / current_session_total * 100
        progress_canvas.coords(progress_fill, 0, 0, 3 * completed, 20)  # 300 px max width
        progress_canvas.itemconfig(progress_text, text=f"{int(completed)}%")

    if count> 0:
        paused_time = count
        timer = window.after(1000,count_down, count-1)
    else:
        start_new_session()
        if reps % 2 == 0:  # Just finished a work session
            work_sessions = math.floor(reps / 2)

            if reps % 8 == 0:
                mark = "✓" * 4
                sets_completed += 1
            else:
                mark = "✓" * (work_sessions % 4)  # ⬅️ Shows up to 4 checkmarks, resets after long break
            checkmark_label.config(text= mark )

        pomodoro_set_label.config(text=f"Pomodoro Sets: {sets_completed}")

        play_sound()

        if reps % 8 == 0:
            show_summary()




# ---------------------------- UI SETUP ------------------------------- #

window =Tk()
window.resizable(False, False)
window.geometry("580x500")
window.title("Pomodoro")
window.config(padx = 100, pady = 50 , bg = YELLOW)

style = ttk.Style()
style.theme_use('default')

style.configure("custom.Horizontal.TProgressbar",
    troughcolor=YELLOW,         # Background of progress bar
    background="#4caf50",       # Green fill (can change later)
    thickness=20,
    bordercolor=YELLOW,
    lightcolor="#4caf50",
    darkcolor="#4caf50"
)


title_label = Label(text ="Let's Pomodoro!", font= (FONT_NAME, 20, "bold"), fg = GREEN, bg = YELLOW, highlightthickness=0)
title_label.grid(column = 1, row = 0)

canvas =Canvas(width = 200, height = 224 , bg = YELLOW,highlightthickness=0)
try:
    tomato_file = resource_path("tomato.png")
    tomato_image = PhotoImage(file=tomato_file)
    canvas.create_image(100, 112, image=tomato_image)
except Exception as e:
    print(f"[Warning] Failed to load image: {e}")
    canvas.create_text(100, 112, text="🍅", fill="black", font=(FONT_NAME, 30, "bold"))
timer_text = canvas.create_text(100,130,text = "00:00", fill = "white", font=(FONT_NAME,40,"bold"))
canvas.grid(column=1, row=2)

start_button = Button(text = "Start",font = (FONT_NAME,12,"normal"),highlightthickness=0, command = start_timer, bg = BUTTON_GREEN, fg = "black")
start_button.grid(row=3, column=0)
start_button.original_bg = BUTTON_GREEN
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)


reset_button = Button(text = "Reset",font = (FONT_NAME,12,"normal"),highlightthickness=0, command=reset_timer, bg = BUTTON_GREEN, fg = "black")
reset_button.grid(row=3,column = 2)
reset_button.original_bg = BUTTON_GREEN
reset_button.bind("<Enter>", on_enter)
reset_button.bind("<Leave>", on_leave)


checkmark_label =Label( fg = GREEN, bg = YELLOW, font = (FONT_NAME, 15,'bold'), highlightthickness=0)
checkmark_label.grid(row = 4, column = 1)

quote_label = Label(text=get_random_motivation_quote(), font=(FONT_NAME, 12), fg="black", bg=YELLOW, wraplength=300, justify="center", height = 2)
quote_label.grid(column=1, row=1, pady=(10, 0))

progress_canvas = Canvas(window, width=300, height=20, bg=YELLOW, highlightthickness=0)
progress_canvas.grid(row=5, column=1, pady=10)

progress_fill = progress_canvas.create_rectangle(0, 0, 0, 20, fill=GREEN, width=0)
progress_text = progress_canvas.create_text(150, 10, text="0%", font=(FONT_NAME, 10, 'bold'), fill="black")




settings_button = Button(command = open_settings,text="⚙️", font=(FONT_NAME, 10), highlightthickness=0,bg ="white", fg = "black")
settings_button.grid(row=0, column=4, sticky="ne", padx=5, pady=5)
settings_button.original_bg = "white"
settings_button.bind("<Enter>", on_enter)
settings_button.bind("<Leave>", on_leave)

pomodoro_set_label = Label(window, text=f"Pomodoro Sets: {sets_completed}", font=(FONT_NAME, 10, "bold"), bg=YELLOW)
pomodoro_set_label.grid(row=6, column=1)



load_user_settings()
window.mainloop()

