import argparse
import sys


def calc(*ip):
    if len(ip) < 2:
        raise TypeError(" Need more ip ")
    ip1 = parse(ip[0])
    cur_mask = [0, 0, 0, 0]
    best_mask = [255, 255, 255, 255]
    for i in range(1, len(ip)):
        ip2 = parse(ip[i])
        cur_mask = get_mask(ip1, ip2)
        if cur_mask < best_mask:
            best_mask = cur_mask.copy()
            best_mask = get_mask(ip1, ip2)
    res = '.'.join(map(str, best_mask)) + '   ' + '.'.join(map(str, get_net(ip1, best_mask)))
    return res


def parse(_str):    #бьем каждый ip на 4 элемента
    buf = _str.split('.')
    buf = [int(x) for x in buf]
    for i in buf:
        if i > 255 or i < 0:
            raise TypeError(" Wrong ip ")
    return buf


def get_mask(_ip1, _ip2):    #ищет маску подсети для двух ip
    mask = [0, 0, 0, 0]
    for i in range(0, 4):
        mask[i] = 255 ^ (_ip1[i] ^ _ip2[i])    #операция эквиваленсии
        if mask[i] < 255:
            string = str(bin(mask[i]))
            if len(string) < 10:  #на случай, если какая-то из масок должна начинаться с нуля...
                mask[i] = 0
                #k=10-len(string)
                #for q in range (0,k):
                #   string=string[:1]+'0'
            else:
                for j in range(2, len(string)):
                    if string[j] == '0':
                        string = string[:j]+string[j:].replace('1', '0')    #обрезаем после первого нуля
                        break
                mask[i] = int(string, 2)
            break
    return mask


def get_net(ip1, mask):  #по маске вычисляет адрес подсети
    net = [0, 0, 0, 0]
    for i in range(0, 4):
        net[i] = ip1[i] & mask[i]
    return net


#ipnew = ['167.128.92.70', '167.128.92.17', '167.128.92.68', '152.139.27.80']
#print(calc(*ipnew))


if __name__ == "__main__":
    ips = []
    for i in range(1, len(sys.argv)):
        ips.append(sys.argv[i])
    print(calc(*ips))



