import pihole as ph
import shodan
import sys
import datetime
import os
import argparse



SHODAN_API_KEY = "Shodan API key Here" # Your Shodan API key :)
shodan = shodan.Shodan(SHODAN_API_KEY)
ip_list = []
b_domain = []
time  = datetime.datetime.now().strftime("%Y-%m-%d %I_%M%p")
file = 'ips {}.txt'.format(time)
bfile = 'blacklist {}.txt'.format(time)
parser = argparse.ArgumentParser(description='Find pi-hole IPs in [Shodan.io]' +
                                    ' and Try to steal Blacklists :) ')
parser.add_argument('-l', '--limit', help='set Number of results', type=int)
args = parser.parse_args()


def shodan_api(limit=0):
    count = 0
    choose = input('\33[33m**Choose search keyword**\n    [1] - pi-hole (recommanded)\n    [2] - pihole\npi-checker~$  \33[0m')
    if choose == '1':
        print('Searching Pi-hole IPs in Shodan ... ')
        for search in shodan.search_cursor('pi-hole'):
            ip = '{}'.format(search['ip_str'])
            ip_list.append(ip)
            count = count + 1
            if count == limit:
                break
        print('{} IPs found!'.format(len(ip_list)))
    elif choose == '2':
        print('Searching Pi-hole IPs in Shodan ... ')
        for search in shodan.search_cursor('pihole'):
            ip = '{}:{}'.format(search['ip_str'], search['port'])
            ip_list.append(ip)
            count = count + 1
            if count == limit:
                break
        print('{} IPs found!'.format(len(ip_list)))
    else:
        print('\033[91mInvaid Number\033[0m')
        sys.exit()



def piholer():
    for ip in ip_list:
        try:
            pihole = ph.PiHole(ip)
            blacklist = pihole.getList("black")
            for burl in blacklist:
                if len(burl) > 0 :
                    print('\33[32m[+]Success: {} -> {} domains\33[0m'.format(ip, len(burl)))
                    for i in burl:
                        b_domain.append(i)
        except:
            print('\033[91m[-]Failed {}\033[0m'.format(ip))
            pass


def save_file(filename, input):
    with open(filename, "w", encoding='utf-8') as f: #ا
        for text in input[::-1]:
            f.write(text+'\n')
        f.close()


def main():
    print('''
 _ __ (_)       ___| |__   ___  ___| | _____ _ __
| '_ \| |_____ / __| '_ \ / _ \/ __| |/ / _ \ '__|
| |_) | |_____| (__| | | |  __/ (__|   <  __/ |
| .__/|_|      \___|_| |_|\___|\___|_|\_\___|_|v1.0
|_|        Twitter & Github :  @ADsecu

            ''')
    mess = '\n\33[33mIPs saved in --> {}\nDomains saven in --> {}\nThanks\33[0m'.format(file, bfile)
    if args.limit:
        shodan_api(args.limit)
        save_file(file, ip_list)
        piholer()
        save_file(bfile, b_domain)
        print(mess)
    elif args.limit is None:
        shodan_api()
        save_file(file, ip_list)
        piholer()
        save_file(bfile, b_domain)
        print(mess)
    else:
        print('''
        USAGE: python3 filnemae.py -l 100
        -l  to set limit for search in shodan !

        ''')


if __name__ == '__main__':
    main()
