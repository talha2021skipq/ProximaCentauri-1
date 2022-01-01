class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        digits.sort()   # We sort the list because we don't want leading zeros
        N = len(digits)
        sol = set()
        for i in range(N):
            if digits[i] !=0:   # 1st digit must not be equal to zero
                for j in range(N): 
                    if i != j:  # Two indices must not be equal
                        for k in range(N):
                            if i != k and j!= k and digits[k] % 2 == 0: # Check if remainder is zero for even numbers
                                sol.add(digits[i] * 100 + digits[j] * 10 + digits[k])
        return sorted(list(sol))