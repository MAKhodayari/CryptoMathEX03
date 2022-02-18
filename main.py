from numpy import zeros
from math import sqrt


def KeyStr2Int(KeyStr):
    Size = int(sqrt(len(KeyStr)))
    KeyInt = zeros((Size, Size), int)
    for i in range(Size):
        for j in range(Size):
            KeyInt[i][j] = int(KeyStr.pop(0))
    KeyInt = KeyInt.tolist()
    return KeyInt


def GenerateKey():
    PrimeFactors = input('Enter prime factors: ').split(' ')
    HyperBlockKey = input('Enter Affine-Hill key values: ').split(' ')
    AffineHillB = input('Enter Affine-Hill B values: ').split(' ')
    KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    AffineHillKey = KeyStr2Int(HyperBlockKey)
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('Prime factors: ' + '\n')
        for Num in PrimeFactors:
            KeyFile.write(Num + ' ')
        KeyFile.write('\n')
        KeyFile.write('Affine-Hill key: ' + '\n')
        for Row in AffineHillKey:
            for Num in Row:
                KeyFile.write(str(Num) + ' ')
            KeyFile.write('\n')
        KeyFile.write('Affine-Hill b: ' + '\n')
        for Num in AffineHillB:
            KeyFile.write(Num + '\n')


def Encrypt():
    pass


def Decrypt():
    pass


def DiscoverKey():
    pass


def Menu():
    print('[1] Key Generation.')
    print('[2] Encryption.')
    print('[3] Decryption.')
    print('[4] Key Discovery.')
    print('[0] Exit.')
    print()


if __name__ == '__main__':
    print('Welcome.')
    print('Please select your desired action from the list below.' + '\n')
    Menu()
    Option = input('Which one do you choose? Option: ')
    print()
    while Option != '0':
        if Option == '1':
            GenerateKey()
            print('Key generation successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '2':
            Encrypt()
            print('Encryption  successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '3':
            Decrypt()
            print('Decryption successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '4':
            DiscoverKey()
            print('Key discovery successful.' + '\n' + 'Anything else?' + '\n')
        else:
            print('Wrong input. Try again.' + '\n')
        Menu()
        Option = input('Which one do you choose? Option: ')
        print()
    print('Thank You.')
