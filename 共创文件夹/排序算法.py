# 快速排序
def quick_sort(low, high, array):
    sentry = array[low]              # 修复②:哨兵只取一次,移到循环外
    while low < high:
        while low < high and array[high] >= sentry:
            high -= 1
        if array[high] < sentry:
            array[low] = array[high]
            low += 1
        while low < high and array[low] <= sentry:
            low += 1
        if array[low] > sentry:
            array[high] = array[low]
            high -= 1
    array[low] = sentry
    return low, high, array

def merge(low, high, array):
    if low < high:                   # 修复③:while 改成 if(循环体只会执行一次)
        left, right = low, high      # 修复①:先记住本次调用的原始边界!!!
        low, high, array = quick_sort(low, high, array)
        merge(left, low - 1, array)  # 左半段:原 low ~ 枢轴前
        merge(high + 1, right, array) # 右半段:枢轴后 ~ 原 high
    return array

def answer(array):
    return merge(0, len(array) - 1, array)

if __name__ == '__main__':
    print(answer([2, 3, 1, 9, 4, 6, 5, 7, 10]))


# 冒泡排序
def bubble_sort(array):
    length = len(array)
    sign =  True
    while sign:
        sign = False
        for i in range(length - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                sign = True
        length -= 1
    return array
if __name__ == '__main__':
    print(bubble_sort([2, 3, 1, 9, 4, 6, 5, 7, 10]))

# 堆排序
def heap_sort(lst):
    k = len(lst)
    while k>1:
        for i in range(k-1,0,-1):
            if lst[i] > lst[(i-1)//2]:        # 构造升序序列 若为<则是逆序序列
                lst[i], lst[(i-1)//2] = lst[(i-1)//2], lst[i]
        lst[0],lst[k-1] = lst[k-1],lst[0]
        k -= 1
    return lst
if __name__ == '__main__':
    a = heap_sort([1,1,3,2,5,8,2,4,9,10,6,7])
    print(a)

# 折半插入法
def binary_insertion_sort(array):
    length = len(array)
    for i in range(length):
        low = 0
        high = i-1
        sentry = array[i]
        while low <= high:
            mid = (low+high)//2
            if sentry < array[mid]:
                high = mid-1
            if sentry >= array[mid]:
                low = mid+1
        for j in range(i-1,low-1,-1):
            array[j+1] = array[j]
        array[low] = sentry
    return array
if __name__ == '__main__':
    print(binary_insertion_sort([2,2,3,1,9,4,6,5,7,10]))


# 直接插入法
def insert_sort(array):
    for i in range(1, len(array)):
        sentry = array[i]
        j = i - 1
        while j >= 0 and array[j] > sentry:   # 边找位置边后移
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = sentry
    return array
if __name__ == '__main__':
    print(insert_sort([2,2,3,1,9,4,6,5,7,10]))


# 训练一
# 寻找一个数组中地K个最大值，重复值不忽略
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def quick_sort(nums,low,high):
            sentry = nums[low]
            while low < high:
                while low<high and nums[high] >= sentry:
                    high -= 1
                if nums[high] < sentry:
                    nums[low] = nums[high]
                    low += 1
                while low<high and nums[low] <= sentry:
                    low += 1
                if nums[low] > sentry:
                    nums[high] = nums[low]
                    high -= 1
            nums[low] = sentry
            return nums,low,high
        def merge(nums,low,high):
            if low < high:
                left,right = low,high
                nums,low,high = quick_sort(nums,low,high)
                if low-len(nums) < -k:
                    return merge(nums,high+1,right)
                if low-len(nums) >  -k:
                    return merge(nums,left,low-1)
                if low-len(nums) == -k:
                    return nums[-k]
            return nums[low]
        def answer(nums):
            low,high = 0,len(nums)-1
            return merge(nums,low,high)
        return answer(nums)
