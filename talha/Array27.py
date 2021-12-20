class Solution(object):
    def removeElement(self, nums, val):
        available_ind=len(nums)-1
        if (nums.count(val)>1):
            for el in nums:   
                try:
                    ind=nums.index(val)
                except: break
                temp=nums[available_ind]
                nums[available_ind]='_'
                nums[ind]=temp               
                available_ind=available_ind-1
        val=nums.count("_")
        for i in range(val):
            nums.remove("_")
        
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        