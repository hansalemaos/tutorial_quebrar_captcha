import os
import re
import tempfile
import time
from ffmpegaudiorecord import start_recording
from audiotranser import transcribe_audio
from touchtouch import touch
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from a_selenium_iframes_crawler import Iframes
from operagxdriver import start_opera_driver


def record_audio(audiofile, ffmpegexe=r"C:\ffmpeg\ffmpeg.exe"):
    audio_data = start_recording(
        ffmpegexe=ffmpegexe, audiodevice=1, silent_seconds_stop=3, silence_threshold=-30
    )
    audio_data.export(audiofile)


def get_wav_tmp():
    suffix = ".wav"
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def get_text_from_audio(audiofile):
    dftext = transcribe_audio(
        inputfile=audiofile,
        small_large="large",
        blas=True,
        silence_threshold=-30,  # ignored if == 0 or None
        min_silence_len=500,  # ignored if silence_threshold == 0 or None
        keep_silence=1000,  # ignored if silence_threshold == 0 or None
        threads=5,  # number of threads to use during computation
        processors=1,  # number of processors to use during computation
        offset_t=0,  # time offset in milliseconds
        offset_n=0,  # segment index offset
        duration=0,  # duration of audio to process in milliseconds
        max_context=-1,  # maximum number of text context tokens to store
        max_len=0,  # maximum segment length in characters
        best_of=2,  # number of best candidates to keep
        beam_size=-1,  # beam size for beam search
        word_thold=0.01,  # word timestamp probability threshold
        entropy_thold=2.40,  # entropy threshold for decoder fail
        logprob_thold=-1.00,  # log probability threshold for decoder fail
        speed_up=False,  # speed up audio by x2 (reduced accuracy)
        translate=False,  # translate from source language to english
        diarize=False,  # stereo audio diarization
        language="en",  # spoken language ('auto' for auto_detect)
    )
    texttowrite = " ".join(
        dftext.drop_duplicates(subset="text").text.str.strip().to_list()
    )
    texttowrite = re.sub(r"[^\w\s]+", " ", texttowrite)
    texttowrite = re.sub(r"\s+", " ", texttowrite).strip()
    print(texttowrite)
    return texttowrite


getiframes = lambda: Iframes(
    driver,
    By,
    WebDriverWait,
    expected_conditions,
    seperator_for_duplicated_iframe="Ç",
    ignore_google_ads=True,
)


driver = start_opera_driver(
    opera_browser_exe=r"C:\Program Files\Opera GX\opera.exe",
    opera_driver_exe=r"C:\ProgramData\anaconda3\envs\dfdir\operadriver.exe",
    userdir="c:\\operabrowserprofile2",
    arguments=(
        "--no-sandbox",
        "--test-type",
        "--no-default-browser-check",
        "--no-first-run",
        "--incognito",
        "--start-maximized",
    ),
)
driver.get(r"https://jurisprudencia.trt15.jus.br/")
time.sleep(5)


def imprimir_elementos():
    driver.switch_to.default_content()
    iframes = getiframes()
    for ini, iframe in enumerate(iframes.iframes):
        try:
            print(f"Frame: {ini} -----------------------------------")
            iframes.switch_to(iframe)
            elemethods = driver.find_elements(By.CSS_SELECTOR, "*")
            print(f"Iframe: {iframe}")
            for ele in elemethods:
                print(ele)
                print(f"{ele.text=}")
                print(f"{ele.tag_name=}")
        except Exception as fe:
            print(fe)
            continue


didweclick = False
while not didweclick:
    driver.switch_to.default_content()
    iframes = getiframes()
    for ini, iframe in enumerate(iframes.iframes):
        try:
            print(f"Frame: {ini} -----------------------------------")
            if """[title="reCAPTCHA"]""" not in iframe:
                continue
            iframes.switch_to(iframe)
            elemethods = driver.find_elements(By.CSS_SELECTOR, "span")
            print(f"Iframe: {iframe}")
            for ele in elemethods:
                try:
                    print(ele)
                    try:
                        ele.click()
                        didweclick = True
                        break
                    except Exception:
                        continue

                except Exception:
                    pass
            if didweclick:
                break
        except Exception as fe:
            print(fe)
            continue


time.sleep(5)
didweclick = False
while not didweclick:
    iframes = getiframes()
    for ini, iframe in enumerate(iframes.iframes):
        try:
            print(f"Frame: {ini} -----------------------------------")
            if """[title="reCAPTCHA"]""" not in iframe:
                continue
            iframes.switch_to(iframe)
            elemethods = driver.find_elements(By.CSS_SELECTOR, "button")
            print(f"Iframe: {iframe}")

            for ele in elemethods:
                try:
                    if "audio" in (ele.get_attribute("outerHTML")):
                        try:
                            ele.click()
                            didweclick = True
                            break
                        except Exception:
                            continue
                except Exception:
                    pass
            if didweclick:
                break
        except Exception as fe:
            print(fe)
            continue

time.sleep(5)
didweclick = False
while not didweclick:
    iframes = getiframes()
    for ini, iframe in enumerate(iframes.iframes):
        try:
            print(f"Frame: {ini} -----------------------------------")
            if """[title="reCAPTCHA"]""" not in iframe:
                continue
            iframes.switch_to(iframe)
            elemethods = driver.find_elements(By.CSS_SELECTOR, "button")
            print(f"Iframe: {iframe}")

            for ele in elemethods:
                try:
                    if ">PLAY<" in (ele.get_attribute("outerHTML")):
                        try:
                            ele.click()
                            didweclick = True
                            break
                        except Exception:
                            continue
                except Exception:
                    pass
            if didweclick:
                break
        except Exception as fe:
            print(fe)
            continue

audiofile = get_wav_tmp()
record_audio(audiofile, ffmpegexe=r"C:\ffmpeg\ffmpeg.exe")
texttowrite = get_text_from_audio(audiofile)

didweclick = False
while not didweclick:
    iframes = getiframes()
    for ini, iframe in enumerate(iframes.iframes):
        try:
            print(f"Frame: {ini} -----------------------------------")
            if """[title="reCAPTCHA"]""" not in iframe:
                continue
            iframes.switch_to(iframe)
            elemethods = driver.find_elements(By.CSS_SELECTOR, "input")
            print(f"Iframe: {iframe}")

            for ele in elemethods:
                try:
                    if 'id="audio-response"' in (ele.get_attribute("outerHTML")):
                        try:
                            ele.send_keys(texttowrite)
                            didweclick = True
                            break
                        except Exception:
                            continue
                except Exception:
                    pass
            if didweclick:
                break
        except Exception as fe:
            print(fe)
            continue


didweclick = False
while not didweclick:
    iframes = getiframes()
    for ini, iframe in enumerate(iframes.iframes):
        try:
            print(f"Frame: {ini} -----------------------------------")
            if """[title="reCAPTCHA"]""" not in iframe:
                continue
            iframes.switch_to(iframe)
            elemethods = driver.find_elements(By.CSS_SELECTOR, "button")
            print(f"Iframe: {iframe}")

            for ele in elemethods:
                try:
                    if ">Verify<" in (ele.get_attribute("outerHTML")):
                        try:
                            ele.click()
                            didweclick = True
                            break
                        except Exception:
                            continue
                except Exception:
                    pass
            if didweclick:
                break
        except Exception as fe:
            print(fe)
            continue
