class Solution:
    def delete_value(self, nums,value):
        if value in nums:
            for i in range (nums.index(value),len(nums)):
                nums[i]=nums[i+1]
        return len(nums)-1
            
            
t=Solution()
arr=[1,2,3,4,5,6]
print(t.delete_value(arr,3))
