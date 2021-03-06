# This is Wilfred, the crypto trading bot
import argparse
import os
import random
import socket
import sys
import time
import urllib.request
from datetime import datetime

import cbpro  # use pip to install (coin base pro)

colors = ['\x1b[0;36;40m'] #,'\x1b[3;31;40m']
red = '\x1b[3;31;40m'
green = '\033[32m'
purp = '\033[1;35m'
lightblue = '\033[94m'
pink = '\x1b[0;35;40m'
gold = '\x1b[7;30;43m'
W = '\033[0m'

logo = '''
                    /\             //|
                   |` \_,--="=--,_//`|
                   \ ."  :'. .':  ". /
                  ==)  _ :  '  : _  (==
                    |>/O\   _   /O\<|
                    | \-"~` _ `~"-/ |
                   >|`===. \_/ .===`|<
             .-"-.   \==='  |  '===/   .-"-.
.-----------{'. '`}---\,  .-'-.  ,/---{.'. '}-----------.
 )          `"---"`     `~-===-~`     `"---"`          (
(          __        ___ _  __              _           )
 )         \ \      / (_) |/ _|_ __ ___  __| |         (
(           \ \ /\ / /| | | |_| '__/ _ \/ _` |          )
 )           \ V  V / | | |  _| | |  __/ (_| |         (
(             \_/\_/  |_|_|_| |_|  \___|\__,_|          )
 )                        #auth - localhost-Security   (
'-------------------------------------------------------'
'''
logo2 = '''
  ____                  _          ____        _
 / ___|_ __ _   _ _ __ | |_ ___   | __ )  ___ | |_
| |   | '__| | | | '_ \| __/ _ \  |  _ \ / _ \| __|
| |___| |  | |_| | |_) | || (_) | | |_) | (_) | |_
 \____|_|   \__, | .__/ \__\___/  |____/ \___/ \__|
            |___/|_|
'''

v_print = None
hostip = socket.gethostbyname(socket.gethostname())
hostname = socket.gethostname()

def login():
    while True:
        try:
            clr()
            parser = argparse.ArgumentParser()
            parser.add_argument('-v', '--verbosity', action="count", 
                            help="increase output verbosity (e.g., -vv is more than -v)\r\n", default=3)

            args = parser.parse_args()

            if args.verbosity:
                def _v_print(*verb_args):
                    if verb_args[0] > (3 - args.verbosity):
                        print(verb_args[1])
            else:
                _v_print = lambda *a: None  # do-nothing function
            global v_print
            v_print = _v_print
             
            import getpass
            user = input(red+f"\r\n[{hostip}]"+W+":Username: ")
            passw = getpass.getpass(red+f"[{hostip}]"+W+":Password: ")
            f = open("config.txt", "r")
            for line in f.readlines():
                us, pw = line.strip().split("|", 1)
                if (user in us) and (passw in pw):
                    print(green+"\r\nLogin successful!"+W)
                    time.sleep(1.3)
                    main()
                else:
                    print(red+"\r\nWrong username/password\r\n"+W)
                    time.sleep(1)
                    #return 0
        except Exception as a:
            print(a)
        except KeyboardInterrupt as e:
            print(e)
            v_print(3, gold+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, gold+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            print(f"See you later {hostip}\r\n")
            sys.exit(1)

def main():
    while True:
        try:
            ts = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            clr()
            v_print(3, gold + f"\r\nINFO - Verbose Mode [ON]\r\nINFO - Logged in as [{hostname}]")
            print(random.choice(colors) + logo + W + green+f"[Version - {verl}]" + f"\t{ts}" + W)

            choice = input(random.choice(colors) + 
            """\n
            * type 'help' to see a list of commands * 
            \r\n""" + gold + f"\r\n[{hostip}]"+W+":"+purp+"wilfred" + W + "> ")
            
            if choice == "bot":
                bot_config()

            elif choice == "list crypto":
                list_cryptos()

            elif choice == "update":
                update()
            
            elif choice == "exit":
                sys.exit(1)

            elif choice == "logout":
                clr()
                v_print(3, gold+"\r\nINFO [*] Logging Out [*]"+W)
                time.sleep(1)
                login()
                break

            elif choice == "help":
                helpdesk("commandlist")

            else:
                print("Please enter a valid command...")
                time.sleep(.8)
                clr()
        except Exception as e:
            print(e)
            v_print(3, gold+"\r\nINFO [*] Something Stopped [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
        except KeyboardInterrupt as a:
            print(a)
            #v_print(3, gold+"\r\nINFO [*] User Exit [*]"+W)
            #v_print(3, gold+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            time.sleep(1)
            print(green+"\r\nFlushing saved Data..."+W)
            time.sleep(1)
            print(red+"Shutting Down Service..."+W)
            time.sleep(1)
            print(red+"Putting Wilfred to Sleep..."+W)
            time.sleep(1)
            print(green+"...............Wilfred was tucked into bed successfully"+W)
            time.sleep(1)
            sys.exit(1) # Exit cleanly

data = open('passphrase.txt', 'r').read().splitlines()
public = data[0]
passphrase = data[1]
secret = data[2]
public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(public, secret, passphrase)

def bot_config():
    while True:
        try:
            clr()
            print(random.choice(colors)+logo2+green+f"[Version - {verl}]" + W)
            global coinchoice
            coinchoice = input(f"\r\nPlease choose a coin to trade by typing its symbol such as...\n\n\t"+green+"[ETH - Etherium]     [BTC - Bitcoin]     [DOGE - Dogecoin]   [SHIB - Shiba Inu]"+W+"\r\n\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> ")
            current_price = float(auth_client.get_product_ticker(product_id=coinchoice+"-USD")['price'])
            global sell_price
            sell_price = float(input(f"\r\nPlease set a sell price based on current {coinchoice} price of {current_price:,}..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global sell_amount
            sell_amount = float(input(f"\r\nPlease set how much of your {coinchoice} you would like to sell\nwhen sell price has been triggered..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global buy_price
            buy_price = float(input(f"\r\nPlease set a buy price..\r\n\n"+green+f"[current {coinchoice} worth - {current_price:,}]\n[currently set sell price - {sell_price:,}]"+W+"\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global buy_amount
            buy_amount = float(input(f"\r\nPlease set a amount of {coinchoice} to buy when buy price of {buy_price:,} has been triggered..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global aggression
            aggression = float(input("\r\nPlease set the aggression..\r\n(1-10) 1 being the most\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            clr()
            print(green+f"[set sell price-{sell_price}] [set sell amount-{sell_amount}] [set buy price-{buy_price}] [set buy amount-{buy_amount}]"+W) # selection headsup
            bot()
        except Exception as i:
            print(i)
            v_print(3, gold+"\r\nINFO [*] Something Stopped [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
            sys.exit(1)
        except KeyboardInterrupt as o:
            print(o)
            main()
            #sys.exit(1) # Exit cleanly

def bot():
    print(gold+"\r\n\t[!] heres a tip... press CTRL+C to stop wilfred from trading and head back to bot config [!]\n"+W)
    while True:
        try:
            ts = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            current_price = float(auth_client.get_product_ticker(product_id=coinchoice+"-USD")['price'])
            if current_price <= buy_price:
                buy_result = green+f"\r\n\t[{ts}]\t[coin - {coinchoice}]\t[buy@{buy_price:,}]\t[sell@{sell_price:,}]"+gold + f"\r\n[{hostip}]~"+W+red+f"Buying {coinchoice}"+W+f" because {coinchoice} price "+purp+f"{current_price:,}"+W+f" fell below buying price limit of "+purp+f"{buy_price:,}"+W
                print(buy_result)
                auth_client.buy(size=buy_amount, order_type="market", product_id=coinchoice+"-USD")
                with open('bought.txt', 'a') as f:
                            print(buy_result, file=f)
                            print("#" * 107 + "\r\n",file=f)
            
            elif current_price >= sell_price:
                sell_result = green+f"\r\n\t[{ts}]\t[coin - {coinchoice}]\t[buy@{buy_price:,}]\t[sell@{sell_price:,}]"+gold + f"\r\n[{hostip}]~"+W+green+f"Selling {coinchoice}"+W+f" because {coinchoice} price "+purp+f"{current_price:,}"+W+f" rose above selling price limit of "+purp+f"{sell_price:,}"+W
                print(sell_result)
                auth_client.sell(size=sell_amount, order_type="market", product_id=coinchoice+"-USD")
                with open('sold.txt', 'a') as f:
                            print(sell_result, file=f)
                            print("#" * 107 + "\r\n",file=f)
            
            else:
                idle = green+f"\r\n\t[{ts}]\t[coin - {coinchoice}]\t[buy@ {buy_price:,}]\t[sell@ {sell_price:,}]"+gold + f"\r\n[{hostip}]~"+W+"Waiting for Trigger! Price is "+purp+f"{current_price:,}!"+W
                print(idle)
            time.sleep(aggression)
        
        except Exception as e:
            v_print(3, gold+"\r\nINFO [*] Something Went Wrong [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
            print(e)
        except KeyboardInterrupt as a:
            print(a)
            #v_print(3, gold+"\r\nINFO [*] User Exit [*]"+W)
            #v_print(3, gold+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            time.sleep(1)
            print(red+f"Host: {hostname}@{hostip} has stopped the bot"+W)
            time.sleep(1)
            print(green+"Flushing bot config Data..."+W)
            time.sleep(1)
            print(green+"returning to bot config...\r\n"+W)
            time.sleep(1)
            bot_config()
            #sys.exit(1)

def list_cryptos():
    while True:
        try:
            result = public_client.get_currencies()
            for row in result:
                print(green+"["+row['id']+"]"+gold+"-----"+row['name']+W)
            #choice = input("\r\nReturn to Main Menu? (y/n)> ")
            crypto = input(f"\r\nType a Crypto like 'BTC' to pull info about it...\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-search/"+W+"> ")
            results = public_client.get_product_ticker(crypto+'-USD')
            print("\n\n"+green)
            print(results)
            print("\n\n"+W)
            time.sleep(1)
            loop_or_not = input("\nWanna look up another? (y/n)> ")
            if loop_or_not == "y":
                list_cryptos()
            elif loop_or_not == "n":
                main()
        except Exception as o:
            print(o)
            v_print(3, gold+"\r\nINFO [*] Something Went Wrong [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
            sys.exit(1)
        except KeyboardInterrupt as k:
            print(k)
            main()


def helpdesk(commlist): 
    if commlist == "commandlist":
        print("\r\nbot\t-\tStart the bot module\nlist crypto\t-\tdisplays a list of all crypto to trade\nupdate\t-\trun a update of the script\nlogout\t-\tlogout\nexit\t-\texit wilfred\nhelp\t-\tdisplays a list of commands\n")
        time.sleep(1)
        choice = input("\r\nReturn to Main Menu? (y/n)> ")
        if choice == "y":
            main()
        elif choice == "n":
            helpdesk("commandlist")
        else:
            print("Please put valid option...")

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'

def update():
    stuff_to_update = ['wilfred.py', '.version', 'requirements.txt', 'README.md', 'config.txt', 'bought.txt', 'sold.txt']
    if ver != verl:
        print('\r\nAn Update is Available....')
        time.sleep(1)
        print('\tStarting Update...')
        time.sleep(1)
        print(green+f"grabbing files: {stuff_to_update}"+gold+"\n\t[*] Expect 7 total file grabs [*]\n"+W)
        for fl in stuff_to_update:
            dat = urllib.request.urlopen("https://raw.githubusercontent.com/localhost-Security/wilfred/master/" + fl).read()
            print(green+"File grabbed..."+W)
            time.sleep(1)
            file = open(fl, 'wb')
            print(gold+"\rWriting Data to File..."+W)
            time.sleep(1)
            file.write(dat)
            file.close()
        print(gold+'\r\nUpdated Successfully...')
        time.sleep(1)
        print('\tPlease Run The Script Again...'+W)
        sys.exit(1)
    
    elif ver == verl:
        print(green+"Your Version is Up-To-Date"+W)
        time.sleep(1)
        print(green+f"Running on Version [{verl}]"+W)
        time.sleep(1)
        print(green+"Heading back now"+W)
        time.sleep(1.2)
        main()

print(gold+'\n\tChecking For Updates...\r\n'+W)
time.sleep(1.5)
ver = urllib.request.urlopen("https://raw.githubusercontent.com/localhost-Security/wilfred/master/.version").read().decode('utf-8')
#verl = get_version()
verl = ''
try:
    verl = open(".version", 'r').read()
except Exception:
    get_version()
    #pass
if ver != verl:
    #print('\r\nAn Update is Available....')
    #print('\tStarting Update...')
    update()
print(green+"Your Version is Up-To-Date"+W)
time.sleep(1)
print(green+f"Running on Version [{verl}]"+W)
time.sleep(1)
print(green+'\rWaking up Wilfred from his nap...\n\n'+W)
time.sleep(1.5)

if __name__ == '__main__':
    login()