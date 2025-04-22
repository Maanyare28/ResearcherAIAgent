import speech_recognition as sr

def listen_to_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Could not request results")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for speech.")
        return None


# Example usage, I want to use the function to listen to a command
if __name__ == "__main__":
    command = listen_to_command()
    if command:
        print(f"Command received: {command}")
    else:
        print("No command received.")