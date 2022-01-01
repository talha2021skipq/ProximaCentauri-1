class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        index = 1
        for i in range(len(nums)-1):    # The first element is fixed, we look at next elements
            if nums[i] != nums[i+1]:    # Comapring two consecutive elements
                nums[index] = nums[i+1] # The last elements don't matter in this example and are ignored 
                index += 1
        return index