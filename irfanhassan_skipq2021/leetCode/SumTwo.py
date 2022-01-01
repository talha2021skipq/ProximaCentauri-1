class Solution:
    def sumtwo(self, nums,target):
        for item in nums:
            if target-item in nums:
                return [nums.index(item),nums.index(target-item)]
        return [-1,-1]    
            
t=Solution()
arr=[1,3,5,6,7]
target=6
print(t.sumtwo(arr,target))