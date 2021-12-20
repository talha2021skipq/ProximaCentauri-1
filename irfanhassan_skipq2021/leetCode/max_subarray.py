import sys
class Solution:
    def maxSubArray(self, nums):
        current_sum=0
        summ=-sys.maxsize-1
        for i in range(len(nums)):
            current_sum=current_sum+nums[i]
            if(summ<current_sum):
                summ=current_sum
            if(current_sum<0):
                current_sum=0
        return summ       
        
        
t=Solution()
arr=[-2,4,6,-3,1,-10,-5]
print(t.maxSubArray(arr))