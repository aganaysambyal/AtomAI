import tkinter as tk
import speech_recognition as sr
import pyttsx3# Import the required module for text
# to speech conversion
import pywhatkit  # for whatsapp,youtube
import datetime
import wikipedia
import pyjokes
import os
import fitz #for pdf
import webbrowser #is a convenient web browser controller

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()
def wishMe(speak):
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning boss")

    elif hour>=12 and hour<18:
        speak("Good Afternoon boss")

    else:
        speak("Good Evening boss")

    speak("I am Atom , tell me what to do")
def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'atom' in command:
                command = command.replace('atom', '')
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        command = take_command()
    except sr.RequestError:
        print('Sorry, I am currently unavailable. Please try again later.')
        command = take_command()
    return command


def read_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text


def send_whatsapp_message():
    global phone_entry, message_entry
    phone_number = phone_entry.get()
    message = message_entry.get()
    pywhatkit.sendwhatmsg(phone_number, message, 12, 21)

if __name__ == "__main__":
    wishMe(pyttsx3.speak)
def run_atom():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The current time is ' + current_time)

    elif 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'open youtube' in command:
        webbrowser.open("youtube.com")

    elif 'open google' in command:
        webbrowser.open("google.com")

    elif 'open stack overflow' in command:
        webbrowser.open("stackoverflow.com")

    elif 'who made you' in command:
        talk('I was created by Mr. Aganay Sambyal.')

    elif 'when you were made' in command:
        talk('I was created on June 11, 2023.')

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'read the pdf' in command:
        book = 'oop.pdf'  # Provide the path to your PDF file here
        text = read_pdf(book)
        print(text)
        talk(text)

    elif 'page' in command:
        book = 'oop.pdf'  # Provide the path to your PDF file here
        with fitz.open(book) as doc:
            total_pages = doc.page_count
            print("Total pages:", total_pages)
            talk(total_pages)

    elif 'whatsapp' in command:
        global phone_entry, message_entry

        root = tk.Tk()
        root.title("WhatsApp Assistant")
        root.configure(background="lightblue")
        root.geometry("1000x500")

        phone_label = tk.Label(root, text="Phone Number:", fg="black", bg="lightblue")
        phone_label.pack(side="top", padx=10, pady=10)
        phone_entry = tk.Entry(root, bg="white")
        phone_entry.pack(side="top", padx=10, pady=10)

        message_label = tk.Label(root, text="Message:", fg="black", bg="lightblue")
        message_label.pack(side="top", padx=10, pady=10)
        message_entry = tk.Entry(root, bg="white")
        message_entry.pack(side="top", padx=10, pady=10)

        send_button = tk.Button(root, text="Send", command=send_whatsapp_message, bg="red", fg="white")
        send_button.pack(side="bottom", padx=10, pady=10)

        root.mainloop()

    elif 'shutdown' in command:
        talk("Goodbye!")
        os.system("shutdown /s /t 1")

    else:
        talk('Sorry, I did not understand that command. Please try again.')


run_atom()

