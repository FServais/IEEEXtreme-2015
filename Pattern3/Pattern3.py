# import re
# """
# public static void main(String[] args) {
#     List<String> inputs = Arrays.asList("AAAAAAAAA", "ABABAB", "ABCAB", "ABAb");
#     for (String s : inputs) System.out.println(findPattern(s));
# }
#
# private static String findPattern(String s) {
#     String output = s;
#     String temp;
#     while (true) {
#         temp = output.replaceAll("(.+)\\1", "$1");
#         if (temp.equals(output)) break;
#         output = temp;
#     }
#     return output;
# }
# """
#
# def find_pattern(s):
#     r = re.compile(r'(.+?)(?=\1)')
#     patterns = r.findall(s)
#     return patterns
#
# def choose_pattern(patterns, s):
#     if not patterns:
#         return s
#     print(patterns)
#     for pattern in patterns:
#         complete = pattern * (len(s) // len(pattern))
#         print("----")
#         print("complete : {}".format(complete))
#         print("s :        {}".format(s))
#         print("----")
#         if len(s) > len(complete):
#             if complete == s[:len(complete)]:
#                 return pattern
#         else:
#             if complete == s:
#                 return pattern
#
#     lengths = list(map(len, patterns))
#     index_min_length = lengths.index(min(lengths))
#     return patterns[index_min_length]
#
# N = int(input())
#
# for _ in range(0, N):
#     s = input()
#     print(choose_pattern(find_pattern(s), s))

def search_pattern(s):
    for l in range(1, (len(s)//2) +1):
        pattern = s[:l]

        complete = pattern * (len(s) // len(pattern))
        # print("----")
        # print("complete : {}".format(complete))
        # print("s :        {}".format(s))
        # print("----")
        if len(s) > len(complete):
            if complete == s[:len(complete)]:
                return pattern
        else:
            if complete == s:
                return pattern

    return s

N = int(input())

for _ in range(0, N):
    s = input()
    print(len(search_pattern(s)))