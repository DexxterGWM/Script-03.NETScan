def clear(_):
    if _: input()
    system('cls')

def getSize(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f'{bytes:.2f}{unit}B'
        bytes /= 1024

def simplified():
    '''
    Simplified View of NET Usage.

    ** FORMATS:
        Upload; Download; Upload download; Download speed.
    '''

    print(colored('\n [*] NET Usage in Simplified Mode.\n', 'green'))

    IO = psutil.net_io_counters()
    bytesSent, bytesRecv = IO.bytes_sent, IO.bytes_recv

    while True:
        time.sleep(1)
        IO2 = psutil.net_io_counters()
        us, ds = IO2.bytes_sent - bytesSent, IO2.bytes_recv - bytesRecv

        print(
f''' Upload: {getSize(IO2.bytes_sent)}    Download: {getSize(IO2.bytes_recv)
    }    Upload download: {getSize(us / 1)}/s    Download speed: {getSize(ds / 1)
}/s''', end='       \r')

        bytesSent, bytesRecv = IO2.bytes_sent, IO2.bytes_recv

def interface():
    '''
    NET Usage Per Interface

    ** FORMATS:
        Iface; Download; Upload; Upload Speed; Download Speed
    '''

    IO = psutil.net_io_counters(pernic = True)

    while True:
        time.sleep(1); data = []
        IO2 = psutil.net_io_counters(pernic = True)

        for iface, ifaceIO in IO.items():
            us, ds = IO2[iface].bytes_sent - ifaceIO.bytes_sent, IO2[iface].bytes_recv - ifaceIO.bytes_recv

            data.append({
                'Iface' : iface, 'Download' : getSize(IO2[iface].bytes_recv), 'Upload' : getSize(IO2[iface].bytes_sent),
                'Upload Speed' : f'{getSize(us / 1)}/s', 'Download Speed' : f'{getSize(ds / 1)}/s'
            })

        IO = IO2

        df = pd.DataFrame(data, index = [f' {i+1}' for i in range(len(IO.items()))])
        df.sort_values('Download', inplace = True, ascending = False)

        clear(''); print(colored('\n [*] NET Usage Per Interface Mode.\n\n', 'green'), df.to_string())

def Print():
    clear(''); cnt, fgr = 0, [
"", "              (`.          ,-,", "              ` `.     ,;' /", "               ` .  ,'/ .'", "                 `. X /.'", "       .-;--''--.._` ` ('",
"     .'           /    `", "    ,          ` '    Q '", "    ,         ,   `._    \\", " ,.|         '     `-.;_'",
" :  . `   ;   `  ` --,.._;\t [?]: CTRL + C", "  ' `     ,  )   .'", "     `._  , '   /_", "        ; ,''-,;' ``-", "         ``-..__``--`"]
    
    for i in range(len(fgr)):
        print(colored(fgr[i], 'red'), end='')
    
        if i in (7, 8):
            cnt += 1; print(f'\t [{colored(cnt, "green")}]: {colored(menu[f"{cnt}"].__name__, "green")}', end='\n')
        elif i == 5: print('\t Functions On This Script:')
        else: print('')

def Get(wht):
    try:
        if wht in menu.keys():
            clear(''); help(menu.get(wht)); clear(' ')
        return menu.get(wht)()

    except KeyboardInterrupt: pass
    except Exception as err:
        input(colored(f'\n [!!] {type(err).__name__} Error: {err}', 'red'))

def main(self):
    Print(); Get(input('\n [*] Select The Function: ')); clear('')

import psutil, time, pandas as pd

from os import system
from termcolor import colored

obj = type('Obj', (object, ), {'main': main, 'simplified': simplified, 'interface': interface})
start, menu = obj(), {'1' : obj.simplified, '2' : obj.interface}

try:
    while True:
        try: clear(''); start.main()
        except Exception as err:
            input(colored(f'\n [!!] {type(err).__name__} Error: {err}', 'red'))

        finally: clear('')

except KeyboardInterrupt: exit(0)
except Exception as err: input(colored(f'\n {type(err).__name__}: {err}.', 'red'))