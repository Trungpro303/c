#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import zipfile
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tSome dependencies could not be imported (possibly not installed)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = """
░░░░░░░░░░░░░░░░▓██████▓▓▓░░░░░░░░░░░░░░░
░░░░░░░░░░░░░█████▓▓█████████▓░░░░░░░░░░░
░░░░░░░░░░█████▓░░▓█████████████░░░░░░░░░
░░░░░░░░▓███▓░░░▓█████████████████░░░░░░░
░░░░░░░███▓░░░░░███████████████████▓░░░░░
░░░░░░███░░░░░░██████████████████████░░░░
░░░░░███░░░░░░░███████████████████████░░░
░░░░███░░░░░░░░███████░░░░██████████▓█▓░░
░░░███▓░░░░░░░░███████░░░░▓██████████▓█░░       ██████╗░██████╗░████████╗
░░▓███░░░░░░░░░░██████▓░░▓███████████▓██░       ██╔══██╗██╔══██╗╚══██╔══╝
░░████░░░░░░░░░░▓████████████████████▓▓█░       ██████╔╝██║░░██║░░░██║░░░
░▓█░█▓░░░░░░░░░░░░████████████████████░██       ██╔═══╝░██║░░██║░░░██║░░░
░██░█░░░░░░░░░░░░░░▓██████████████████░██       ██║░░░░░██████╔╝░░░██║░░░
░█▓░█░░░░░░░░░░░░░░░░░▓███████████████░▓█       ╚═╝░░░░░╚═════╝░░░░╚═╝░░░ #by PhamDuyThai
▓█▓░█▓░░░░░░░░░░░░░░░░░░██████████████░░█
██░░██░░░░░░░░░░░▓▓░░░░░░▓████████████░░█
██░▓░█░░░░░░░░░░████▓░░░░░███████████▓░░█
██░█░██░░░░░░░░▓█████░░░░░░██████████░░▓█
██░▓█░██░░░░░░░░████▓░░░░░░█████████░░▓▓█
▓█░░█░░█▓░░░░░░░░▓▓░░░░░░░░████████▓░░▓██
░█░░█▓░▓██░░░░░░░░░░░░░░░░░███████▓░░█▓█▓       ░██████╗██████╗░░█████╗░███╗░░░███╗
░██░███████▓░░░░░░░░░░░░░░██████████▓█▓█░       ██╔════╝██╔══██╗██╔══██╗████╗░████║
░▓█░██▓░░░▓███░░░░░░░░░░▓██████▓░░░▓██▓█░       ╚█████╗░██████╔╝███████║██╔████╔██║
░░███▓░░░░░░░███████████████▓░░░░░░░░██▓░       ░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║
░░░██░░▓▓█▓▓▓░░░▓████████▓░░░░▓▓█▓▓░░██░░       ██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║
░░░▓█░████████▓░░░░░░░░░░░░▓████████░▓█░░       ╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝ #https://www.facebook.com/925873
░░░█▓▓███████████░░░░░░░░████████████░█▓░
░░░█░█████████████░░░░░░█████████████░██░
░░▓█░▓████████████░░░░░░█████████████░░█░
░░▓█░▓▓███████████░░░░░░███████████▓▓░░█░
░░▓█░░░▓█████████░░░░░░░░█████████▓░░░░█░
░░░█▓░░░████████░░░░░░░░░░████████░░░░██░
░░░██░░░░░█████░░░░████░░░░█████▓░░░░░█▓░
░░░░██░░░░░░░░░░░░██████░░░░░░░░░░▓░░██░░
░░░░▓████▓░░░░░░░░███▓██▓░░░░░░░░█████░░░       ████████╗░█████╗░░█████╗░██╗░░░░░
░░░░░▓█▓████▓░░░░░██░▓▓██░░░░▓████░██░░░░       ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░░░░░░░▓█▓██░▓░░░██▓▓▓██░░█▓█████░░░░░░░       ░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░░░░░░▓█░███▓░░░▓▓▓░▓░░░░░█▓██▓█░░░░░░░       ░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░░░░░░▓█░██▓░░▓░░░░░░░░░▓░███▓▓█░░░░░░░       ░░░██║░░░╚█████╔╝╚█████╔╝███████╗
░░░░░░░░▓█░███▓███▓░░░░░▓███▓██░▓█░░░░░░░       ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝ #zalo (có cc t đưa cho spam :v)
░░░░░░░░██░░██░▓░█████████░▓▓█▓░▓█░░░░░░░
░░░░░░░░▓█░░▓██▓▓░░▓░█░█░▓░▓██░░░█░░░░░░░
░░░░░░░░░█▓░░████░▓░░▓░░▓▓███░░░██░░░░░░░
░░░░░░░░░▓█▓░░████████▓█████░░░██▓░░░░░░░
░░░░░░░░░░░██░░▓▓▓▓▓▓▓▓▓▓▓█░░░██░░░░░░░░░
░░░░░░░░░░░░██░░▓█████▓██▓░░▓██░░░░░░░░░░
░░░░░░░░░░░░░██░░░░░▓▓░░░░░███░░░░░░░░░░░
░░░░░░░░░░░░░░██░░░░░░░░░░██▓░░░░░░░░░░░░
░░░░░░░░░░░░░░▓██░░░░░░░░██░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░██████████░░░░░░░░░░░░░░░
                                         """
    if ASCII_MODE:
        logo = ""
    version = "Version: "+__VERSION__
    contributors = "Contributors: "+" ".join(__CONTRIBUTORS__)
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    mesgdcrt.SectionMessage(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Poor internet connection detected")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def do_zip_update():
    success = False
    if DEBUG_MODE:
        zip_url = "https://github.com/TheSpeedX/TBomb/archive/dev.zip"
        dir_name = "TBomb-dev"
    else:
        zip_url = "https://github.com/TheSpeedX/TBomb/archive/master.zip"
        dir_name = "TBomb-master"
    print(ALL_COLORS[0]+"Downloading ZIP ... "+RESET_ALL)
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_content = response.content
        try:
            with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
                for member in zip_file.namelist():
                    filename = os.path.split(member)
                    if not filename[1]:
                        continue
                    new_filename = os.path.join(
                        filename[0].replace(dir_name, "."),
                        filename[1])
                    source = zip_file.open(member)
                    target = open(new_filename, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
            success = True
        except Exception:
            mesgdcrt.FailureMessage("Error occured while extracting !!")
    if success:
        mesgdcrt.SuccessMessage("TBomb was updated to the latest version")
        mesgdcrt.GeneralMessage(
            "Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update TBomb.")
        mesgdcrt.WarningMessage(
            "Grab The Latest one From https://github.com/TheSpeedX/TBomb.git")

    sys.exit()


def do_git_update():
    success = False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL, end='')
        process = subprocess.Popen("git checkout . && git pull ",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL, end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except Exception:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("TBomb was updated to the latest version")
        mesgdcrt.GeneralMessage(
            "Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update TBomb.")
        mesgdcrt.WarningMessage("Make Sure To Install 'git' ")
        mesgdcrt.GeneralMessage("Then run command:")
        print(
            "git checkout . && "
            "git pull https://github.com/TheSpeedX/TBomb.git HEAD")
    sys.exit()


def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()


def check_for_updates():
    if DEBUG_MODE:
        mesgdcrt.WarningMessage(
            "DEBUG MODE Enabled! Auto-Update check is disabled.")
        return
    mesgdcrt.SectionMessage("Checking for updates")
    fver = requests.get(
        "https://raw.githubusercontent.com/TheSpeedX/TBomb/master/.version"
    ).text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("An update is available")
        mesgdcrt.GeneralMessage("Starting update...")
        update()
    else:
        mesgdcrt.SuccessMessage("TBomb is up-to-date")
        mesgdcrt.GeneralMessage("Starting TBomb")


def notifyen():
    try:
        if DEBUG_MODE:
            url = "https://github.com/TheSpeedX/TBomb/raw/dev/.notify"
        else:
            url = "https://github.com/TheSpeedX/TBomb/raw/master/.notify"
        noti = requests.get(url).text.upper()
        if len(noti) > 10:
            mesgdcrt.SectionMessage("NOTIFICATION: " + noti)
            print()
    except Exception:
        pass


def get_phone_info():
    while True:
        target = ""
        cc = input(mesgdcrt.CommandMessage(
            "Nhập mã quốc gia của bạn (Without +): "))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "The country code ({cc}) that you have entered"
                " is invalid or unsupported".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            "Nhập Số Điện Thoại: +" + cc + " "))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "The phone number ({target})".format(target=target) +
                "that you have entered is invalid")
            continue
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("Nhập Mail Muốn Spam: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "The mail ({target})".format(target=target) +
                " that you have entered is invalid")
            continue
        return target


def pretty_print(cc, target, success, failed):
    requested = success+failed
    mesgdcrt.SectionMessage("Bombing is in progress - Please be patient")
    mesgdcrt.GeneralMessage(
        "Please stay connected to the internet during bombing")
    mesgdcrt.GeneralMessage("Mục Tiêu       : " + cc + " " + target)
    mesgdcrt.GeneralMessage("Số Lần Gửi         : " + str(requested))
    mesgdcrt.GeneralMessage("Số LầnThành công   : " + str(success))
    mesgdcrt.GeneralMessage("Số Lần Thất Bại      : " + str(failed))
    mesgdcrt.WarningMessage(
        "Công cụ này được tạo ra chỉ dành cho mục đích vui vẻ và spam chet con đĩ nic :v")
    mesgdcrt.SuccessMessage("TBomb was created by SpeedX")


def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    mesgdcrt.SectionMessage("Gearing up the Bomber - Please be patient")
    mesgdcrt.GeneralMessage(
        "Please stay connected to the internet during bombing")
    mesgdcrt.GeneralMessage("API Version   : " + api.api_version)
    mesgdcrt.GeneralMessage("Mục Tiêu        : " + cc + target)
    mesgdcrt.GeneralMessage("Số lượng        : " + str(count))
    mesgdcrt.GeneralMessage("Threads       : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("Delay         : " + str(delay) +
                            " seconds")
    mesgdcrt.WarningMessage(
        "Công cụ này được tạo ra chỉ dành cho mục đích vui vẻ và spam chet con đĩ nic :v")
    print()
    input(mesgdcrt.CommandMessage(
        "Nhấn [CTRL + Z] để tạm dừng hoặc [ENTER] để tiếp tục"))

    if len(APIProvider.api_providers) == 0:
        mesgdcrt.FailureMessage("Quốc gia / mục tiêu của bạn chưa được hỗ trợ")
        mesgdcrt.GeneralMessage("Vui lòng liên hệ với chúng tôi")
        input(mesgdcrt.CommandMessage("Bấm [ENTER] Để Thoát"))
        bann_text()
        sys.exit()

    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    mesgdcrt.FailureMessage(
                        "Bombing limit for your target has been reached")
                    mesgdcrt.GeneralMessage("Try Again Later !!")
                    input(mesgdcrt.CommandMessage("Press [ENTER] to exit"))
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                pretty_print(cc, target, success, failed)
    print("\n")
    mesgdcrt.SuccessMessage("Bombing completed!")
    time.sleep(1.5)
    bann_text()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        notifyen()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                message = ("Nhập Số Lần {type}".format(type=mode.upper()) +
                           " Muốn Spam (Max {limit}): ".format(limit=limit))
                count = int(input(mesgdcrt.CommandMessage(message)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("You have requested " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "Automatically capping the value"
                        " to {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage("Enter delay time (in seconds): "))
                    .strip())
                # delay = 0
                max_thread_limit = (count//10) if (count//10) > 0 else 1
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        "Nhập Số Luồng (Recommended: {max_limit}): "
                        .format(max_limit=max_thread_limit)))
                    .strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("Read Instructions Carefully !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Received INTR call - Exiting...")
        sys.exit()


mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("TBomb will work only in Python v3")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    update()


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['Phạm Duy Thái']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

ASCII_MODE = False
DEBUG_MODE = False

description = """TBomb - Your Friendly Spammer Application

TBomb can be used for many purposes which incudes -
\t Exposing the vulnerable APIs over Internet
\t Friendly Spamming
\t Testing Your Spam Detector and more ....

TBomb is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Coded by SpeedX !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="start TBomb with SMS BOMB mode")
parser.add_argument("-call", "--call", action="store_true",
                    help="start TBomb with CALL Bomb mode")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="start TBomb with MAIL Bomb mode")
parser.add_argument("-ascii", "--ascii", action="store_true",
                    help="show only characters of standard ASCII set")
parser.add_argument("-u", "--update", action="store_true",
                    help="update TBomb")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="show current TBomb contributors")
parser.add_argument("-v", "--version", action="store_true",
                    help="show current TBomb version")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.ascii:
        ASCII_MODE = True
        mesgdcrt = MessageDecorator("stat")
    if args.version:
        print("Version: ", __VERSION__)
    elif args.contributors:
        print("Contributors: ", " ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {
            "1": "SMS",
            "2": "CALL",
            "3": "MAIL"
        }
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print("Vui lòng chọn chức năng ⚡️:\n")
                for key, value in avail_choice.items():
                    print("[ {key} ] {value} BOMB".format(key=key,
                                                          value=value))
                print()
                choice = input(mesgdcrt.CommandMessage("Enter Choice : "))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("Received INTR call - Exiting...")
            sys.exit()
    sys.exit()
