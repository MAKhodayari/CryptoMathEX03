from numpy import zeros, array, add, matmul, subtract, sqrt


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
                    Temp.append(Row[i:i + Size])
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
    Factor = list()
    if Number % 2 == 0:
        Factor.append(2)
    for i in range(3, Number + 1, 2):
        if Number % i == 0 and Prime(i):
            Factor.append(i)
    return Factor


def ModularDivision(Rows, Factors, Mode):
    Remainder = list()
    for Row in Rows:
        Temp1 = list()
        for Mat in Row:
            Temp2 = list()
            for Col in Mat:
                Temp3 = list()
                for Num in Col:
                    if Mode == 'B':
                        Temp3.append(Num % Factors)
                    elif Mode == 'PF':
                        for Factor in Factors:
                            Temp3.append(Num % Factor)
                Temp2.append(Temp3)
            Temp1.append(Temp2)
        Remainder.append(Temp1)
    return Remainder


def SoloBlock(Rows, Size):
    HyperBlock = list()
    for Row in Rows:
        # AppendedRow = ''.join(Row)
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


def AffineHill(Rows, Key, B, Base, Mode):
    Temp = list()
    for Mat in Rows:
        if Mode == 'E':
            Temp.append(add(matmul(Key, Mat), B).tolist())
        elif Mode == 'D':
            Temp.append(matmul(Key, subtract(Mat, B)).tolist())
    AffineHillRes = ModularDivision(Temp, Base, 'B')
    return AffineHillRes


def KeyStr2Int(KeyStr):
    Size = int(sqrt(len(KeyStr)))
    KeyInt = zeros((Size, Size), int)
    for i in range(Size):
        for j in range(Size):
            KeyInt[i][j] = int(KeyStr.pop(0))
    KeyInt = KeyInt.tolist()
    return KeyInt


def GenerateKey():
    Base = input('Enter base number N: ')
    HyperBlockKey = input('Enter Affine-Hill key values: ').split(' ')
    AffineHillB = input('Enter Affine-Hill B values: ').split(' ')
    # KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    KeyPath = r'C:\Users\User\Desktop\T3\Key.txt'
    AffineHillKey = KeyStr2Int(HyperBlockKey)
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('N: ' + Base + '\n')
        KeyFile.write('Affine-Hill key: ' + '\n')
        for Row in AffineHillKey:
            for Num in Row:
                KeyFile.write(str(Num) + ' ')
            KeyFile.write('\n')
        KeyFile.write('Affine-Hill b: ' + '\n')
        for Num in AffineHillB:
            KeyFile.write(Num + '\n')


def ExtractKeyInfo(Path):
    with open(Path, 'r') as File:
        Info = list()
        for Row in File.readlines():
            Info.append(Row.strip().split(' '))
    N = int(Info[0][-1])
    PrimeFactors = Factorize(N)
    Size = len(Info[2])
    AffineHillKey = list()
    for Row in Info[2:2 + Size]:
        AffineHillKey.append(list(Row))
    for i in range(len(AffineHillKey)):
        for j in range(len(AffineHillKey[i])):
            AffineHillKey[i][j] = int(AffineHillKey[i][j])
    AffineHillB = list()
    for Num in Info[3 + Size:]:
        AffineHillB.append(int(Num[0]))
    AffineHillB = array(AffineHillB).reshape(-1, 1).tolist()
    return N, PrimeFactors, AffineHillKey, AffineHillB


def Encrypt():
    # KeyPath = input('Enter key location: ')
    # FilePath = input('Enter original file location: ')
    # ASCIIFilePath = input('Enter location to save original file in ASCII format: ') + '\OriginalASCII.txt'
    # EncryptedPath = input('Enter location to save encrypted file: ') + '\Encrypted.txt'
    KeyPath = r'C:\Users\User\Desktop\T3\Key.txt'
    FilePath = r'C:\Users\User\Desktop\T3\1.txt'
    ASCIIFilePath = r'C:\Users\User\Desktop\T3\OriginalASCII.txt'
    EncryptedPath = r'C:\Users\User\Desktop\T3\Encrypted.txt'
    N, PrimeFactors, AffineHillKey, AffineHillB = ExtractKeyInfo(KeyPath)
    CharD = ExtractFileInfo(FilePath, 'EA')
    CharH = SoloBlock(CharD, len(AffineHillKey))
    CharAH = AffineHill(CharH, AffineHillKey, AffineHillB, N, 'E')
    CharR = ModularDivision(CharAH, PrimeFactors, 'PF')
    with open(EncryptedPath, 'w') as EncryptedFile:
        for Row in CharR:
            for Mat in Row:
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
    print(ExtractFileInfo(EncryptedPath, 'ER', len(PrimeFactors)))


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
    # a = ExtractFileInfo(r'C:\Users\User\Desktop\T3\1.txt', 'EA')
    # b, c, d, e = ExtractKeyInfo(r'C:\Users\User\Desktop\T3\Key.txt')
    # f = ModularDivision(a, c)
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)
    # print(f)
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
