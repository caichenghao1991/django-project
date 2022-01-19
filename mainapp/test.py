class Solution:
    """
    @param num1: a non-negative integers
    @param num2: a non-negative integers
    @return: return sum of num1 and num2
    """

    def addStrings(self, num1, num2):
        # write your code here
        add, res = 0, []

        s, l = (num1, num2) if len(num1) < len(num2) else (num2, num1)
        print(s, l)
        add = 0
        p1, p2 = len(s) - 1, len(l) - 1

        print(p1, p2)
        while (p1 != 0 or p2 != 0):
            print(type(p1))

            a = 0
            if p1 > 0:
                a = int(s[p1])
            r = (a + int(l[p2]) + add) % 10
            res.append(str(r))
            print(res, p1, p2)
            if (a + int(l[p2]) + add) >= 10:
                add = 1
            p1 = p1 - 1
            p2 = p2 - 1
        if add == 1: res.append('1')
        return ''.join(reversed(res))
s = Solution()
s.addStrings('12','345')