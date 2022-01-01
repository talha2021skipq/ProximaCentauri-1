class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        a = {}      # A dictionary to keep track of a number
        for i in nums:
            if i in a:
                a[i] += 1
            else:
                a[i] = 1
        for key, value in a.items():    # dict.items() returns a 
            if value == 1:
                return key