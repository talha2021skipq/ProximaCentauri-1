class Solution:
    def searchInsert(self, nums, target):
        nums.append(target)
        return list(sorted(set(nums))).index(target)
        
    

t=Solution()
arr=[2,3,5,6,7]
target=5
print(t.searchInsert(arr,target))