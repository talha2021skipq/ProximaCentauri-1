class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        marker = 0
        for i in range(len(s)):
            s.insert(marker,s[-1])
            s.pop()
            marker += 1