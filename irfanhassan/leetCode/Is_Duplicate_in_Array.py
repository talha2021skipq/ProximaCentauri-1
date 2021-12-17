#irfanskipq2021
#check if thre is any number is multiple time in array

def is_duplicate(nums):
    n=len(nums)
    for i in range(0,n):
        for j in range(i+1,n):
            if (nums[i]==nums[j]):
                return True
    return False
        
arr=[1,2,3,4,16,5,6,9,10,12]
print(is_duplicate(arr))