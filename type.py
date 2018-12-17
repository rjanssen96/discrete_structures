global homogeneous
index = ""

def find_n(s,ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def find_type(homogeneous):
    with open("C:/Users/RikvB/PycharmProjects/discrete_structures/input_files/comass03.txt", "r") as f:
        for i in range(3):
            line = f.readline()
        print("line = " + line)

    index = find_n(line, "n")
    print(index)
    s_pos = []
    count = 0

    for j in index:
        print("number = " + str(j))
        print("number -2 = " + str(j-2))
        s_pos.append(count)
        s_pos[count] = j - 2
        count = count+1
    print(index)
    print(s_pos)

    for k in s_pos:
        if line[k] == "s":
            print("CORRECT " + str(k))
            homogeneous = True
            continue
        else:
            print("NOPE " + str(k))
            homogeneous = False
            break
    return homogeneous

homogeneous = find_type(homogeneous=False)
print(homogeneous)