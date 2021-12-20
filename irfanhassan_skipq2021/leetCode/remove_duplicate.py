class Solution:
    def removeDuplicates(self, nums):
        if len(nums) == 0 or len(nums) == 1:
            return len(nums)
        else: 
            arr=[]
            for i in nums:
                if i not in arr:
                    arr.append(i)
            return arr
            
            
t=Solution()
arr=[1,2,3,4,1,2,3]
print(t.removeDuplicates(arr))
