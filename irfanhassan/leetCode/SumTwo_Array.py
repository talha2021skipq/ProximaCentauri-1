#irfanskipq
#to get index of number in array whose sum is equal to given target number
class Solution:
    def twoSum(self, nums, target):
        for x in nums:
            firstNum = nums.index(x)
            nums[firstNum] = "a"
            if target - x in nums:
                return [firstNum,nums.index(target - x)]
                

obj=Solution()
arr=[3,5,7,9,10]
target=12
print(obj.twoSum(arr,target))