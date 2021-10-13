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
                    time.sleep(1.5)
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
            clr()
            v_print(3, gold + f"\r\nINFO - Verbose Mode [ON]\r\nINFO - Logged in as [{hostname}]")
            print(random.choice(colors) + logo + W + green+f"[Version - {verl}]" + W)

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
            v_print(3, pink+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, pink+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            print(f"See you later {hostip}\r\n")
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
            current_price = float(auth_client.get_product_ticker(product_id="BTC-USD")['price'])
            global sell_price
            sell_price = float(input(f"\r\nPlease set a sell price based on current BTC price of {current_price:,}..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global sell_amount
            sell_amount = float(input("\r\nPlease set how much of your BTC you would like to sell\nwhen sell price has been triggered..\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
            global buy_price
            buy_price = float(input(f"\r\nPlease set a buy price..\r\n\n"+green+f"[current BTC worth - {current_price:,}]\n[currently set sell price - {sell_price:,}]"+W+"\r\n\r\n"+gold+ f"[{hostip}]"+W+":"+purp+"wilfred"+W+red+"/crypto-bot/"+W+"> "))
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
            sys.exit(1)
        except KeyboardInterrupt as o:
            print(o)
            v_print(3, pink+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, pink+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            print(f"See you later {hostip}\r\n")
            main()
            #sys.exit(1) # Exit cleanly

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
                main()
            elif loop_or_not == "n":
                list_cryptos()
        except Exception as o:
            print(o)
            v_print(3, gold+"\r\nINFO [*] Something Went Wrong [*]"+W)
            v_print(3, gold+"WARN [*] Exception has occured [*]\r\n"+W)
            sys.exit(1)
        except KeyboardInterrupt as k:
            print(k)
            v_print(3, gold+"\r\nINFO [*] User Exit [*]"+W)
            v_print(3, gold+"WARN [*] KeyboardInterrupt [*]\r\n"+W)
            main()


def helpdesk(commlist): 
    if commlist == "commandlist":
        print("\r\nbot\t-\tStart the bot module\nlist crypto\t-\tdisplays a list of all crypto to trade\nupdate\t-\trun a update of the script\nlogout\t-\tlogout\nexit\t-\texit wilfred\nhelp\t-\tdisplays a list of commands\n")
        time.sleep(3)
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
    stuff_to_update = ['wilfred.py', '.version', 'requirements.txt']
    if ver != verl:
        print('\r\nAn Update is Available....')
        print('\tStarting Update...')
        for fl in stuff_to_update:
            dat = urllib.request.urlopen("https://raw.githubusercontent.com/localhost-Security/wilfred/master/" + fl).read()
            file = open(fl, 'wb')
            file.write(dat)
            file.close()
        print(gold+'\r\nUpdated Successfully...')
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