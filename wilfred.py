# This is Wilfred, the crypto trading bot
import argparse
import os
import random
import socket
import sys
import time
import urllib.request

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
 )                                         v1.0.0      (
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
                    print("\r\nLogin successful!")
                    time.sleep(1.5)
                    main()
                else:
                    print("\r\nWrong username/password\r\n")
                    time.sleep(1)
                    return 0
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
            clr()
            v_print(3, gold + f"\r\nINFO - Verbose Mode [ON]\r\nINFO - Logged in as [{hostname}]")
            print(random.choice(colors) + logo + W)

            choice = input(random.choice(colors) + 
            """\r\n
            * type 'bot' to enter the bot module 
            * type 'logout' to logout 
            * type 'exit' to leave 
            \r\n""" + gold + f"\r\n[{hostip}]"+W+":"+purp+"wilfred" + W + "> ")
            
            if choice == "bot":
                bot_config()
            
            elif choice == "exit":
                sys.exit(1)

            elif choice == "logout":
                clr()
                v_print(3, gold+"\r\nINFO [*] Logging Out [*]"+W)
                time.sleep(1)
                login()
                break
            
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
            v_print(3, pink+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, pink+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            print(f"See you later {hostip}\r\n")
            sys.exit(1) # Exit cleanly

data = open('passphrase.txt', 'r').read().splitlines()
public = data[0]
passphrase = data[1]
secret = data[2]

auth_client = cbpro.AuthenticatedClient(public, secret, passphrase)

def bot_config():
    while True:
        try:
            clr()
            print(random.choice(colors)+logo2)
            current_price = float(auth_client.get_product_ticker(product_id="BTC-USD")['price'])
            global sell_price
            sell_price = float(input(f"\r\nPlease set a sell price based on current BTC price of {current_price:,}..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global sell_amount
            sell_amount = float(input("\r\nPlease set how much of your BTC you would like to sell\nwhen sell price has been triggered..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global buy_price
            buy_price = float(input(f"\r\nPlease set a buy price..\r\n\n[current BTC worth - {current_price:,}]\n[currently set sell price - {sell_price:,}]\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global buy_amount
            buy_amount = float(input(f"\r\nPlease set a amount of BTC to buy when buy price of {buy_price:,} has been triggered..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global aggression
            aggression = float(input("\r\nPlease set the aggression..\r\n(1-10) 1 being the most\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            clr()
            print(green+f"[set sell price-{sell_price}] [set sell amount-{sell_amount}] [set buy price-{buy_price}] [set buy amount-{buy_amount}]"+W) # selection headsup
            bot()
        except Exception as i:
            print(i)
            v_print(3, gold+"\r\nINFO [*] Something Stopped [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
        except KeyboardInterrupt as o:
            print(o)
            v_print(3, pink+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, pink+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            print(f"See you later {hostip}\r\n")
            sys.exit(1) # Exit cleanly

def bot():
    while True:
        try:
            current_price = float(auth_client.get_product_ticker(product_id="BTC-USD")['price'])
            if current_price <= buy_price:
                buy_result = gold + f"\r\n[{hostip}]~"+W+red+f"Buying BTC"+W+f" because BTC price "+purp+f"{current_price:,}"+W+f" fell below buying price limit of "+purp+f"{buy_price:,}"+W
                print(buy_result)
                auth_client.buy(size=buy_amount, order_type="market", product_id="BTC-USD")
                with open('bought.txt', 'a') as f:
                            print(buy_result, file=f)
                            print("#" * 107 + "\r\n",file=f)
            
            elif current_price >= sell_price:
                sell_result = gold + f"\r\n[{hostip}]~"+W+green+f"Selling BTC"+W+f" because BTC price "+purp+f"{current_price:,}"+W+f" rose above selling price limit of "+purp+f"{sell_price:,}"+W
                print(sell_result)
                auth_client.sell(size=sell_amount, order_type="market", product_id="BTC-USD")
                with open('sold.txt', 'a') as f:
                            print(sell_result, file=f)
                            print("#" * 107 + "\r\n",file=f)
            
            else:
                idle = gold + f"\r\n[{hostip}]~"+W+f"Waiting for Trigger! Price is {current_price:,}!"
                print(idle)
            time.sleep(aggression)
        
        except Exception as e:
            v_print(3, gold+"\r\nINFO [*] Something Went Wrong [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
            print(e)
        except KeyboardInterrupt as a:
            print(a)
            v_print(3, gold+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, gold+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            print(f"See you later {hostip}\r\n")
            sys.exit(1)

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def update():
    stuff_to_update = ['wilfred.py', '.version']
    for fl in stuff_to_update:
        dat = urllib.request.urlopen("https://raw.githubusercontent.com/localhost-Security/wilfred/master/" + fl).read()
        file = open(fl, 'wb')
        file.write(dat)
        file.close()
    print(gold+'\r\nUpdated Successfull !!!!')
    print('\tPlease Run The Script Again...'+W)
    sys.exit(1)

print(gold+'\n\tChecking For Updates...\r\n'+W)
ver = urllib.request.urlopen("https://raw.githubusercontent.com/localhost-Security/wilfred/master/.version").read().decode('utf-8')
verl = ''
try:
    verl = open(".version", 'r').read()
except Exception:
    pass
if ver != verl:
    print('\r\nAn Update is Available....')
    print('\tStarting Update...')
    update()
print("Your Version is Up-To-Date")
print(gold+'\r\Waking up Wilfred from his nap...\n\n'+W)

if __name__ == '__main__':
    login()
