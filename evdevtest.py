def find_second_to_last(haystack, needle):
    found = []
    for i, e in enumerate(haystack):
        if e == needle:
            found.append(i)

    print(found)
    if len(found) >= 2:
        return found[-2]
    else:
        return found[-1]

print(find_second_to_last(['te', 'asf'], 'asf'))
