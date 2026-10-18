def kmp_search(string, patt):
# 假设我们已经算出了 next 数组(马上讲到)

    next = build_next(patt)

    i=0 # 主串中的指针
    j=0 #子串中的指针
    while i < len(string):
        if string[i] == patt[j]: #字符匹配,指针后移
            i += 1
            j += 1
        elif j >0:              #字符失配,根据 next 跳过子串前面的一些字符
            j = next[j-1]
        else:                   #子串第一个字符就失配
            i += 1

        if j == len(patt):      # 匹配成功
            return i - j


def build_next(patt):


    #计算 Next 数组

    prefix_len = 0 #当前共同前后缀的长度
    i = 1

    next=[0] #next 数组(初值元素一个0)
    

    while i < len(patt) :
        if patt[prefix_len] == patt[i]:
            prefix_len += 1
            next. append(prefix_len)
            i += 1
        else:
            if prefix_len == 0:
                next. append(0)
                i += 1
            else:
                prefix_len = next[prefix_len - 1]

    return next


# 练习1
# P3375 【模板】KMP

## 题目描述(汇总)
"""
给定两个字符串 s1 和 s2，求：
1. s2 在 s1 中所有出现的位置 l（区间 [l,r] 的子串与 s2 完全相同）
2. s2 每个前缀的最长 border 长度（border：既是字符串的前缀、又是其后缀，且不等于字符串本身的子串）

输入格式：第一行为 s1，第二行为 s2
输出格式：先按从小到大每行一个输出 s2 在 s1 中所有出现的位置；
最后一行输出 len(s2) 个整数，第 i 个整数为 s2 长度为 i 的前缀的最长 border 长度。
"""

def build_next(patt):
    next = [0]
    length = len(patt)
    i = 1
    prefix_len = 0
    while i < length:
        if patt[prefix_len] == patt[i]:
            prefix_len += 1
            i += 1
            next.append(prefix_len)
        else:
            if prefix_len == 0:
                next.append(0)
                i += 1
            else:
                prefix_len = next[i-1]
    return next
def kmp(string,patt):
    i = j = 0
    ans = []
    length1 = len(string)
    length2 = len(patt)
    while i < length1:
        if string[i] == patt[j]:
            i += 1
            j += 1
        elif j == 0:
            i += 1
        else:
            j = next[j-1]
        if j == length2:
            ans.append(i-j)
            j = next[j-1]
    return ans


string = input().strip()
patt = input().strip()
next = build_next(patt)
ans = kmp(string,patt)
for i in ans:
    print(i+1)
for j in next:
    print(j,end=" ")
