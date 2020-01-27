from gtts import gTTS
import pygame

def text_to_speech(content):
    tts = gTTS(text = content, lang='zh-cn')
    tts.save("media/content.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("media/content.mp3")
    pygame.mixer.music.play(0)

    while pygame.mixer.music.get_busy():
        pass
