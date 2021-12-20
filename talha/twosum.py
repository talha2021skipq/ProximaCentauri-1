class Solution(object):
    def twoSum(self, nums, target):
        required = {}
        for i in range(len(nums)):
          if target - nums[i] in required:
             return [required[target - nums[i]],i]
          else:
            required[nums[i]]=i
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        