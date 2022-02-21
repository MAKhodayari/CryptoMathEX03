from numpy import zeros, array, add, matmul, subtract
from math import prod, sqrt
from sympy import Matrix


def ExtractFileInfo(Path, Mode, Size=1):
    CharCode = list()
    if Mode == 'EA':
        with open(Path, 'rb') as File:
            for Row in File.readlines():
                CharCode.append(list(Row.strip()))
    elif Mode == 'ER':
        with open(Path, 'r') as File:
            for Row in File.readlines():
                Row = Row.strip().split(' ')
                Temp = list()
                for i in range(0, len(Row), Size):
                    Temp.append(array(Row[i:i + Size]).reshape((Size, 1)).tolist())
                CharCode.append(Temp)
    return CharCode


def Prime(Number):
    if Number < 2:
        return False
    elif Number == 2:
        return True
    else:
        for i in range(3, int(sqrt(Number)) + 1, 2):
            if Number % i == 0:
                return False
        return True


def Factorize(Number):
    Factor = set()
    if Number % 2 == 0:
        Factor.add(2)
    for i in range(3, Number + 1, 2):
        if Number % i == 0 and Prime(i):
            Factor.add(i)
    Factor = list(Factor)
    return Factor


def ModularDivision(Mats, Factor):
    Remainder = list()
    for Mat in Mats:
        Temp2 = list()
        for Col in Mat:
            Temp1 = list()
            for Num in Col:
                Temp1.append(Num % Factor)
            Temp2.append(Temp1)
        Remainder.append(Temp2)
    return Remainder


# def ModularDivision(Rows, Factors, Mode):
#     Remainder = list()
#     if Mode == 'AHK':
#         for Row in Rows:
#             Temp1 = list()
#             for Num in Row:
#                 Temp2 = list()
#                 for Factor in Factors:
#                     Temp2.append(Num % Factor)
#                 Temp1.append(Temp2)
#             Remainder.append(Temp1)
#     elif Mode == 'AHB':
#         for Num in Rows:
#             Temp = list()
#             for Factor in Factors:
#                 Temp.append(int(Num) % Factor)
#             Remainder.append(Temp)
#     else:
#         for Row in Rows:
#             Temp1 = list()
#             for Mat in Row:
#                 Temp2 = list()
#                 for Col in Mat:
#                     Temp3 = list()
#                     for Num in Col:
#                         if Mode == 'B':
#                             Temp3.append(Num % Factors)
#                         elif Mode == 'PF':
#                             for Factor in Factors:
#                                 Temp3.append(Num % Factor)
#                     Temp2.append(Temp3)
#                 Temp1.append(Temp2)
#             Remainder.append(Temp1)
#     return Remainder


def SoloBlock(Rows, Size):
    HyperBlock = list()
    for Row in Rows:
        BlockTemp = list()
        if len(Row) % Size == 0:
            Count = len(Row) // Size
        else:
            Count = len(Row) // Size + 1
        for c in range(Count):
            Temp = zeros((Size, 1), int)
            for i in range(Size):
                if len(Row) != 0:
                    Temp[i][0] = Row[0]
                    Row = Row[1:]
            BlockTemp.append(Temp.tolist())
        HyperBlock.append(BlockTemp)
    return HyperBlock


def Block(Rows, Size):
    a = list()
    for Row in Rows:
        t = list()
        for i in range(0, len(Row), Size):
            t.append(Row[i:i + Size])
        a.append(t)
    return a


def AffineHill(Rows, Keys, Bs, Bases, Mode):
    Res = list()
    for Row in Rows:
        Temp2 = list()
        for Mat in Row:
            Temp1 = list()
            for i in range(len(Bases)):
                if Mode == 'E':
                    Temp1.append(add(matmul(Keys[i], Mat), Bs[i]).tolist())
                elif Mode == 'D':
                    Temp1.append(matmul(Keys[i], subtract(Mat, Bs[i])).tolist())
                Temp1 = ModularDivision(Temp1, Bases[i])
            Temp2.append(Temp1)
        Res.append(Temp2)
    return Res


def KeyStr2Int(KeyStr):
    Size = int(sqrt(len(KeyStr)))
    KeyInt = zeros((Size, Size), int)
    for i in range(Size):
        for j in range(Size):
            KeyInt[i][j] = int(KeyStr.pop(0))
    KeyInt = KeyInt.tolist()
    return KeyInt


def BlockStr2Int(BlockStr):
    BlockInt = list()
    for Row in BlockStr:
        Temp1 = list()
        for Char in Row:
            Temp2 = list()
            for Mat in Char:
                Temp3 = list()
                for Col in Mat:
                    Temp4 = list()
                    for Num in Col:
                        Temp4.append(int(Num))
                    Temp3.append(Temp4)
                Temp2.append(Temp3)
            Temp1.append(Temp2)
        BlockInt.append(Temp1)
    return BlockInt


def MatInv(Mats, Bases):
    Inv = list()
    for i in range(len(Bases)):
        Inv.append(Matrix(Mats[i]).inv_mod(Bases[i]).tolist())
    return Inv


def SolveCRT(Rows, Factors):
    P = prod(Factors)
    N = list()
    Y = list()
    for Factor in Factors:
        N.append(P // Factor)
        Y.append(pow(N[-1], -1, Factor))
    Num = list()
    for Row in Rows:
        Temp = list()
        for Remainders in Row:
            Res = 0
            for i in range(len(Remainders)):
                Res += int(Remainders[i]) * N[i] * Y[i]
            Temp.append(Res % P)
        Num.append(Temp)
    return Num


def wtf(Rows, Factors, Mode):
    Ans = list()
    for Factor in Factors:
        Temp = list()
        if Mode == 'K':
            for Row in Rows:
                for Num in Row:
                    Temp.append(Num % Factor)
            Ans.append(array(Temp).reshape(len(Rows), len(Rows)).tolist())
        elif Mode == 'B':
            for Num in Rows:
                Temp.append(int(Num) % Factor)
            Ans.append(array(Temp).reshape(len(Rows), 1).tolist())
    return Ans


def GenerateKey():
    # N = input('Enter base number N: ')
    # AffineHillKeySTR = input('Enter Affine-Hill key values: ').split(' ')
    # AffineHillB = input('Enter Affine-Hill B values: ').split(' ')
    # KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    N = '210'
    AffineHillKeySTR = '10 25 41 87 110 97 203 141 23'.split(' ')
    AffineHillB = '150 109 48'.split(' ')
    KeyPath = r'C:\Users\User\Desktop\T3\Key.txt'
    PrimeFactors = Factorize(int(N))
    AffineHillKey = KeyStr2Int(AffineHillKeySTR)
    AffineHillKeyCRT = wtf(AffineHillKey, PrimeFactors, 'K')
    AffineHillBCRT = wtf(AffineHillB, PrimeFactors, 'B')
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('N: {}\n'.format(N))
        for KeyCRT in AffineHillKeyCRT:
            KeyFile.write('Affine-Hill Key [{}]:\n'.format(AffineHillKeyCRT.index(KeyCRT)))
            for Row in KeyCRT:
                for Num in Row:
                    KeyFile.write(str(Num) + ' ')
                KeyFile.write('\n')
        for BCRT in AffineHillBCRT:
            KeyFile.write('Affine-Hill B [{}]:\n'.format(AffineHillBCRT.index(BCRT)))
            for Row in BCRT:
                for Num in Row:
                    KeyFile.write(str(Num) + ' ')
                KeyFile.write('\n')


def ExtractKeyInfo(Path):
    with open(Path, 'r') as File:
        Info = list()
        for Row in File.readlines():
            Info.append(Row.strip().split(' '))
    N = int(Info[0][-1])
    PrimeFactors = Factorize(N)
    AffineHillSize = len(Info[2])
    AffineHillInfo = list()
    for i, Row in enumerate(Info):
        if Row[0] == 'Affine-Hill':
            AffineHillInfo.append(i)
    for i in range(len(AffineHillInfo) // 2):
        AffineHillKeys = list()
        for AHI in AffineHillInfo[:i + 1]:
            Temp = list()
            for Row in Info[AHI + 1:AHI + 4]:
                for Num in Row:
                    Temp.append(int(Num))
            AffineHillKeys.append(array(Temp).reshape((AffineHillSize, AffineHillSize)).tolist())
        AffineHillBs = list()
        for AHI in AffineHillInfo[i + 1:]:
            Temp = list()
            for Row in Info[AHI + 1:AHI + 4]:
                for Num in Row:
                    Temp.append(int(Num))
            AffineHillBs.append(array(Temp).reshape((AffineHillSize, -1)).tolist())
    return N, PrimeFactors, AffineHillKeys, AffineHillBs


def Encrypt():
    # KeyPath = input('Enter key location: ')
    # FilePath = input('Enter original file location: ')
    # ASCIIFilePath = input('Enter location to save original file in ASCII format: ') + '\OriginalASCII.txt'
    # EncryptedPath = input('Enter location to save encrypted file: ') + '\Encrypted.txt'
    KeyPath = r'C:\Users\User\Desktop\T3\Key.txt'
    FilePath = r'C:\Users\User\Desktop\T3\1.txt'
    ASCIIFilePath = r'C:\Users\User\Desktop\T3\OriginalASCII.txt'
    EncryptedPath = r'C:\Users\User\Desktop\T3\Encrypted.txt'
    N, PrimeFactors, AffineHillKeys, AffineHillBs = ExtractKeyInfo(KeyPath)
    CharD = ExtractFileInfo(FilePath, 'EA')
    print(CharD)
    CharH = SoloBlock(CharD, len(AffineHillKeys[0][0]))
    print(CharH)
    CharAH = AffineHill(CharH, AffineHillKeys, AffineHillBs, PrimeFactors, 'E')
    print(CharAH)
    with open(EncryptedPath, 'w') as EncryptedFile:
        for Row in CharAH:
            for Char in Row:
                for Mat in Char:
                    for Col in Mat:
                        for Num in Col:
                            EncryptedFile.write(str(Num) + ' ')
            EncryptedFile.write('\n')
    with open(ASCIIFilePath, 'w') as ASCIIFile:
        for Row in CharD:
            for Num in Row:
                ASCIIFile.write(str(Num) + ' ')
            ASCIIFile.write('\n')


def Decrypt():
    # KeyPath = input('Enter key location: ')
    # EncryptedPath = input('Enter Encrypted file location: ')
    # # Save location for decrypted text file
    # DecryptedPath = input('Enter location to save decrypted file: ') + '\Decrypted.txt'
    # ASCIIDecryptedPath = input('Enter location to save ASCII decrypted file: ') + '\DecryptedASCII.txt'
    KeyPath = r'C:\Users\User\Desktop\T3\Key.txt'
    EncryptedPath = r'C:\Users\User\Desktop\T3\Encrypted.txt'
    DecryptedPath = r'C:\Users\User\Desktop\T3\Decrypted.txt'
    ASCIIDecryptedPath = r'C:\Users\User\Desktop\T3\DecryptedASCII.txt'
    N, PrimeFactors, AffineHillKey, AffineHillB = ExtractKeyInfo(KeyPath)


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
