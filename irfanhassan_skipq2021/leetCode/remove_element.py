class SolutionWithForLoop:
    def removeElement(self, nums, val):
        index = 0
        while index < len(nums):
            if nums[index] == val:
                del nums[index]
            else:
                index += 1
        return len(nums)
        
        
t=SolutionWithForLoop()
arr=[2,3,1,4,5,2,3]
t.removeElement(arr,3)
print(arr)