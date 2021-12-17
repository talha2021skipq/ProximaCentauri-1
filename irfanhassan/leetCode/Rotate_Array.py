#irfanskipq2021
#rotate array to right by given number

def rotate(nums, k):
    length = len(nums)
    k = k % length
    nums[:] = nums[length - k : length] + nums[:length - k]
    return nums
        
arr=[1,2,3,4,5,6]
num=3
new_arrr=rotate(arr,2)
print(new_arrr)