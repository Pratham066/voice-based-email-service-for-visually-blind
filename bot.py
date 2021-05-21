import speech_recognition as sr
import pyttsx3


class As:
    def __init__(user, id, rate = 150, voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0", threshold = 550):
        user._id = id
        user._rate = rate
        user.voice = voice
        user.r = sr.Recognizer()
        user.r.energy_threshold = threshold
        user.r.dynamic_energy_threshold = True
        user.command = None
    
    def get_id(user):
        return user._id
    
    def set_id(user, id):
        user._id = id
    
    def get_recognized_audio(user):
        return user.command
    
    def set_recognized_audio(user, arg):
        user.command = arg

    def speak(user,text):
        try:
            engine = pyttsx3.init()
            engine.setProperty("voice", user.voice)
            engine. setProperty("rate", user._rate)
            engine.say(text)
            engine.runAndWait()
        except Exception as ex:
            return ex

    def listen(user, text = "", timeLimit = 5):
        try:
            with sr.Microphone() as source:
                user.speak(text)
                user.r.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = user.r.listen(source, phrase_time_limit = timeLimit)
                    return user.r.recognize_google(audio)
                except:
                    # user.speak("I wasn't able to hear anything")
                    return ""
        except Exception as ex:
            return ex
    
    def callback(user, recognizer, audio):
        try:
            # user.r.adjust_for_ambient_noise(source, duration=1)
            recognized = user.r.recognize_google(audio)
            user.command = recognized
            # print(user.command)
            return recognized
        except Exception as ex:
            user.command = ""
            return ""

    def listen_constantly(user):
        mic = sr.Microphone()
        stopper = user.r.listen_in_background(mic, user.callback, phrase_time_limit = 5)
        return stopper