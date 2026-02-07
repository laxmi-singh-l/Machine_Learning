import pyttsx3
from pyttsx3 import engine 
import setuptools

engine = pyttsx3.init()

num = int(input("Enter a number: "))
result = num * num

print("Square:", result)
engine.say(f"The square of {num} is {result}")

engine.runAndWait()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

engine.setProperty('rate', 150)     # speed
engine.setProperty('volume', 1.0)   # volume

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice (usually)


nums = [1,3,-1,-3,5,3,6,7]
k = 3
output = [3,3,5,5,6,7]

print(output)
speak(f"The sliding window maximum output is {output}")
