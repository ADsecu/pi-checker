import pihole as ph
import shodan
import sys
import datetime
import os
import argparse



SHODAN_API_KEY = "Shodan API key Here" # Your Shodan API key :)
shodan = shodan.Shodan(SHODAN_API_KEY)
ip_list = []
content = []
time  = datetime.datetime.now().strftime("%Y-%m-%d %I_%M%p")
Rfile = 'Result {}.txt'.format(time)
parser = argparse.ArgumentParser(description='Find pi-hole IPs in [Shodan.io]' +
                                    ' and Try to steal Blacklists :) ')
parser.add_argument('-l', '--limit', help='set Number of results', type=int)
parser.add_argument('-t', '--target', help='set target IP ')
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
            core = pihole.getVersion()['core_current']
            web = pihole.getVersion()['web_current']
            FTL = pihole.getVersion()['FTL_current']
            blacklist = pihole.getList("black")
            content.append('\n\nIP -> {}\ninfo -> Core {} | web {} | FTL {}'.format(ip, core, web, FTL))
            for burl in blacklist:
                if len(burl) > 0 :
                    print('\33[32m[+]Success: {} -> {} domains\33[0m'.format(ip, len(burl)))
                    for i in burl:
                        content.append('   {}'.format(i))

        except:
            print('\033[91m[-]Failed {}\033[0m'.format(ip))
            pass


def save_file(filename, input):
    this_folder = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(this_folder, filename)
    with open(file_name, "w", encoding='utf-8') as f: #ا
        for text in input:
            f.write(text+'\n')
        f.close()


def main():
    print('''
 _ __ (_)       ___| |__   ___  ___| | _____ _ __
| '_ \| |_____ / __| '_ \ / _ \/ __| |/ / _ \ '__|
| |_) | |_____| (__| | | |  __/ (__|   <  __/ |
| .__/|_|      \___|_| |_|\___|\___|_|\_\___|_|v1.1
|_|        Twitter & Github :  @ADsecu

            ''')
    mess = '\n\33[33mIPs & Domains saved in --> {}\nThanks\33[0m'.format(Rfile)
    if args.limit:
        shodan_api(args.limit)
        piholer()
        save_file(Rfile, content)
        print(mess)
    elif args.target:
        ip_list.append(args.target)
        piholer()
        save_file(Rfile, content)
        print(mess)
    elif args.limit is None:
        shodan_api()
        piholer()
        save_file(Rfile, content)
        print(mess)
    else:
        print('''
        Something Wrong :)
        ''')


if __name__ == '__main__':
    main()
