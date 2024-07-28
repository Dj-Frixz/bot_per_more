import keyboard
from configparser import ConfigParser
from time import sleep

config_dict = ConfigParser()
config_dict.read('config.ini')

def main():
    CREDENTIALS = config_dict['CREDENTIALS']

    if CREDENTIALS['number'] == '':
        setup()
    
    print('Open the website on Tor in fullscreen, '
          'when ready press <F5> then, when the page has loaded, press <F2>.\n'
          'To stop it press down <F2> until the bot has stopped.\n')
    keyboard.wait('f2')

    #try:
    mainloop(config_dict['SETUP'], CREDENTIALS['email'], int(CREDENTIALS['k']),
             CREDENTIALS['password'], int(CREDENTIALS['number']))
    #except:
    save()
    #    input('Exited for unexpected error in mainloop.')
    
def setup():
    config_dict['CREDENTIALS']['email'] = input(
        'Insert your known email, substituting the unknown characters with '
        'an equal amount of # (ex. bruh###@gmail.com for bruh000..., bruh001, etc.): '
    )
    config_dict['CREDENTIALS']['k'] = str(config_dict['CREDENTIALS']['email'].count('#'))
    config_dict['CREDENTIALS']['password'] = input('Insert your password: ')
    config_dict['CREDENTIALS']['number'] = '0'
    print('\nSaving info in config.ini... ', end='')
    save()

def mainloop(SETUP, EMAIL, K, PSSW, n):
    TABS = int(SETUP['tabs_to_email'])
    TRIES = int(SETUP['num_of_tries'])
    UPDATE_IP = SETUP['update_ip']
    EMAIL = EMAIL.split('#'*K)
    if len(EMAIL)!=2: raise ValueError
    LIMIT = 10**K
    DELAY1 = float(config_dict['SETUP']['delay_between_tries'])
    DELAY2 = float(config_dict['SETUP']['delay_between_ip_updates'])
    DELAY3 = float(config_dict['SETUP']['delay_typing'])

    while n<LIMIT:
        for _ in range(TRIES):
            keyboard.send('tab,'*(TABS-1)+'tab')
            keyboard.write(EMAIL[0]+str(n).zfill(K)+EMAIL[1], delay=DELAY3)
            keyboard.send('tab')
            keyboard.write(PSSW, delay=DELAY3)
            keyboard.send('enter')
            n += 1
            config_dict['CREDENTIALS']['number'] = str(n)
            sleep(DELAY1)
            if keyboard.is_pressed('f2'):
                return
        
        keyboard.send('ctrl+shift+l')
        sleep(DELAY2)

def save():
    with open('config.ini', 'w') as config_file:
        config_dict.write(config_file)
    print('Saved!\n')

if __name__=='__main__':
    main()