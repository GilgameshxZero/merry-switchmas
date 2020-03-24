import sys
import getopt
import requests
import bs4
import re
import time
import traceback
import datetime
from lib import lib


def main(argv):
    """
    Every few seconds, check https://www.bhphotovideo.com/c/product/1553451-REG/nintendo_switch_animal_crossing_new.html to see if the product is available.
    """
    PRODUCT_URLS = [
        "https://www.bhphotovideo.com/c/product/1552396-REG/nintendo_switch_animal_crossing_new.html",
        "https://www.bhphotovideo.com/c/product/1553451-REG/nintendo_switch_animal_crossing_new.html",
        "https://www.bhphotovideo.com/c/product/1553452-REG/nintendo_switch_animal_crossing_new.html",
        "https://www.bhphotovideo.com/c/product/1553453-REG/nintendo_switch_animal_crossing_new.html",
        "https://www.bhphotovideo.com/c/product/1553473-REG/nintendo_switch_animal_crossing_new.html",
    ]
    CHECK_PERIOD_S = 15
    COOLDOWN_S = 600

    # Parse command line arguments.
    try:
        opts, args = getopt.getopt(argv, "", ["token=", "sms="])
        opts = {opt[0]: opt[1] for opt in opts}
    except:
        print("Error parsing command-line arguments. Continuing...")
        opts = {}

    # SMS.
    stdlib = lib(token=opts["--token"])
    sms = stdlib.utils.sms["@1.0.11"]

    in_stock = False
    while not in_stock:
        for url in PRODUCT_URLS:
            try:
                soup = bs4.BeautifulSoup(requests.get(
                    url, timeout=60).text, "html.parser")
                buttons = list(soup.select(
                    "button[data-selenium=\"addToCartButton\"]"))
            except:
                traceback.print_exc()
                print("Something went wrong while scraping… Cooling down…")
                time.sleep(COOLDOWN_S)
            if len(buttons) > 0:
                # Send Merry an SMS.
                print(datetime.datetime.now(), "Product", url, "is available. Sending SMS…")
                in_stock = True
                try:
                    sms_result = sms(
                        to=opts["--sms"],
                        body="Nintendo Switch AC available now at " + url
                    )
                    print(sms_result)
                except:
                    traceback.print_exc()
                    print("Something went wrong while sending SMS… Cooling down…")
                    time.sleep(COOLDOWN_S)
        if not in_stock:
            print(datetime.datetime.now(), "Did not find available product.")
            time.sleep(CHECK_PERIOD_S)
        else:
            print("Exiting…")


if __name__ == "__main__":
    main(sys.argv[1:])
