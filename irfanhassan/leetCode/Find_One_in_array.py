#irfanskipq2021
#Find number which are only single time in array

def Find_One(nums):
    for nm in nums:
        if (nums.count(nm)==1):
            print(nm)
    return nm
        
arr=[1,2,3,1,2,4,5]
print(Find_One(arr))