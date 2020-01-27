#import random
import time
import speech_recognition as sr
from speech import text_to_speech

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # Read from serial for listening
    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            print("1/3: 我正在聽呢 ... ...")
            start_time = time.time()
            recognizer.dynamic_energy_threshold = False
            audio = recognizer.listen(source, timeout = 2.0, phrase_time_limit = 2.0)
            print("我聽完了，一共花了 %s 秒！" % (time.time() - start_time))
        except Exception as e:
            response["success"] = False
            response["error"] = e
            return response

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    # update the response object accordingly
    start_time = time.time()

    try:
        print("2/3: 我正在思考您說的是什麼 ... ...")
        response["transcription"] = recognizer.recognize_google(audio, language='zh-TW')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"

    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "我的 Google 語音辨識好像失效了！"

    print("3/3: 我猜完了，一共花了 %s 秒！" % (time.time() - start_time))
    
    return response


if __name__ == "__main__":
    while True:
        # Write reset to serial
        recognizer = sr.Recognizer()
        microphone = sr.Microphone(chunk_size=1024, sample_rate=48000)

        text_to_speech("我是黃媽媽百科全書!請問你要煮什麼？")
        guess = recognize_speech_from_mic(recognizer, microphone)

        # if there was an error, stop the game
        if guess["error"]:
            text_to_speech("雖然我是小神童，可是我聽不懂你再說什麼？")
            continue

        # show the user the transcription
        text_to_speech("你說: {}".format(guess["transcription"]) + " 嗎?這個小神童會做！")

        line_list = [line.rstrip('\n') for line in open("books/炒蘑菇.txt")]
        for obj in line_list:
            text_to_speech(obj)

            if "完成" in obj:
                break

            text_to_speech("準備好了請說:下一步！")
            while True:
                guess = recognize_speech_from_mic(recognizer, microphone)
                print("你說: {}".format(guess["transcription"]))
                if guess["transcription"] != None and "下一步" in guess["transcription"]:
                     break

                time.sleep(0.5) 
