print('__   ________  _____  ______                   ')
print('\ \ / /| ___ \/  ___| |  _  \    (_)           ')
print(' \ V / | |_/ /\ `--.  | | | |_ __ ___   _____  ')
print(' /   \ |  __/  `--. \ | | | | \'__| \ \ / / _ \ ')
print('/ /^\ \| |    /\__/ / | |/ /| |  | |\ V /  __/ ')
print('\/   \/\_|    \____/  |___/ |_|  |_| \_/ \___| ')
print('\n' + 'X-ray photoelectron spectroscopy data processing')
print('Author: Viktor V. Yagodin, Yekaterinburg, Russia')
print('Feedback, wishes and curses send to Viktor.V.Yagodin@gmail.com')
print('Version 1.0')
print('\n'+'______________________________________________________________')


def auger():
    print('Select X-ray gun anode:')
    print('Mg, 1253.6 eV - 0 or any key')
    print('Al, 1486.6 eV - 1')
    sel = input('Anode: ')
    if sel == '1':
        xe = 1486.6
        print('Al anode')
    else:
        xe = 1253.6
        print('Mg anode')
    ae = float(input('Auger line energy E(A), eV: '))
    be = float(input('Electron binding energy E(e), eV: '))
    print('')
    print('Auger parameter (α-parameter) is', round(xe - ae + be, 2), 'eV')


def start():
    print('')
    print(' 1 - help')
    print(' 2 - prepare raw data files')
    print(' 3 - calculate relative concentrations')
    print(' 4 - calculate auger parameter')
    print(' 5 - exit')
    print('')
    command = input('Enter command: ')
    if command == '1':
        f = open('readme.txt')
        print(f.read())
        f.close()
        start()
    elif command == '2':
        import prepare
        start()
    elif command == '3':
        import Conc
        start()
    elif command == '4':
        print('Auger parameter (α-parameter) calculator')
        print('')
        auger()
        start()
    elif command == '5':
        exit()
    else:
        print('bad command')
        start()


start()
