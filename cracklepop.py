#python 3.5
num = 1
while num <= 100:
        if (num % 3) == 0 and (num % 5) == 0:
            print('CracklePop')
        elif (num % 3) == 0:
            print('Crackle')
        elif (num % 5) == 0:
            print('Pop')
        num += 1