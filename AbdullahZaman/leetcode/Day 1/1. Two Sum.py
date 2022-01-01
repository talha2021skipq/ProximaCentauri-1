class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # a dictionary having elements of nums as keys and indices as values
        values = {}
        for i in range(len(nums)):
            """if element is in the list, 
            return a list of value of that key 
            and the current index""" 
            if nums[i] in values:
                return [values[nums[i]], i]
            else:
                """ We take the difference of target 
                and the current element to make sure 
                the desired element is in the array and 
                store it in a dictinoary along with the current index"""
                values[target-nums[i]] = i
        return None