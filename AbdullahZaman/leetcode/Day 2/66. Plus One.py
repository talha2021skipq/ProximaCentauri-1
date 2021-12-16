class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        string_digits = ""
        new_list = []
        for i in digits:    # Converting a list of numbers to a number string
            string_digits += str(i)
        int_digits = int(string_digits) + 1     # Incrementing the integer by 1
        int_digits = str(int_digits)
        for i in int_digits:        # Appending digits to list
            new_list.append(int(i))
        return new_list