def removeElement(nums, val):
    arr=[]
    length = len(nums)
    i = 0
    while i < length:
        if nums[i] == val:
            for j in range (i,length-1):
                nums[j]=nums[j+1]
            break
        else:
            i += 1
    return length-1
    
arr=[1,2,3,4,5,6,7,8,9]
val=5
n=removeElement(arr,val)
for i in range (n):
    print(arr[i])