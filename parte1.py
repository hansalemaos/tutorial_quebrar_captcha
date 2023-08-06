import random
import rapidfuzz
import undetected_chromedriver as uc
import pandas as pd
from time import sleep
import pytesseract
from PrettyColorPrinter import add_printer
import numpy as np

add_printer(1)
import mousekey

mkey = mousekey.MouseKey()
mkey.enable_failsafekill("ctrl+e")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from fast_ctypes_screenshots import (
    ScreenshotOfOneMonitor,
)


def get_screenshot_tesser(minlen=2):
    with ScreenshotOfOneMonitor(
        monitor=0, ascontiguousarray=True
    ) as screenshots_monitor:
        img5 = screenshots_monitor.screenshot_one_monitor()
    df = pytesseract.image_to_data(img5, output_type="data.frame")
    df = df.dropna(subset="text")
    df = df.loc[df.text.str.len() > minlen].reset_index(drop=True)
    return df


def move_mouse(
    x,
    y,
    variationx=(-5, 5),
    variationy=(-5, 5),
    up_down=(0.2, 0.3),
    min_variation=-10,
    max_variation=10,
    use_every=4,
    sleeptime=(0.009, 0.019),
    linear=90,
):
    mkey.left_click_xy_natural(
        int(x) - random.randint(*variationx),
        int(y) - random.randint(*variationy),
        delay=random.uniform(*up_down),
        min_variation=min_variation,
        max_variation=max_variation,
        use_every=use_every,
        sleeptime=sleeptime,
        print_coords=True,
        percent=linear,
    )


if __name__ == "__main__":
    options = uc.ChromeOptions()
    userdir = "c:\\chromeprofiletest"
    options.add_argument(f"--user-data-dir={userdir}")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get(r"https://jurisprudencia.trt15.jus.br/")
    sleep(20)
    df = get_screenshot_tesser(minlen=2)
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                rapidfuzz.process_cpp.cdist(["Imnot", "arobot"], df.text.to_list())
            ).T.rename(columns={0: "imnot", 1: "arobot"}),
        ],
        axis=1,
    )

    try:
        vamosclicar = (
            np.diff(
                df.loc[
                    ((df.imnot == df.imnot.max()) & (df.imnot > 90))
                    | ((df.arobot == df.arobot.max()) & (df.arobot > 90))
                ][:2].index
            )[0]
            == 1
        )
    except Exception:
        vamosclicar = False

    if vamosclicar:
        x, y = df.loc[df.imnot == df.imnot.max()][["left", "top"]].__array__()[0]
        move_mouse(
            x,
            y,
            variationx=(-10, 10),
            variationy=(-10, 10),
            up_down=(0.2, 0.3),
            min_variation=-10,
            max_variation=10,
            use_every=4,
            sleeptime=(0.009, 0.019),
            linear=90,
        )
