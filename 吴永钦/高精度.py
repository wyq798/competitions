# 和小学的加法运算一样，先加再进位 
def add(a1,a2):
    array = []
    s = 0

    while a1!=[] and a2!=[] or s!=0:
        m = a1.pop() if a1!=[] else 0
        n = a2.pop() if a2!=[] else 0
        array.append(str((m+n+s)%10))
        s = (m+n+s)//10    # 减法只需要把m+n写成m-n
    if a1 != []:
        array.extend(str(a1[::-1]))
    if a2 != []:
        array.extend(a2[::-1])
    array = [str(x) for x in array[::-1]]
    return ''.join(array)

if __name__ == '__main__':
    s1 = input()
    s2 = input()
    s1 = [int(x) for x in s1]
    s2 = [int(x) for x in s2]
    print(add(s1,s2))

              