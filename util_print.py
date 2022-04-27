def to_alphabet(num):
    if (num == None):
        return '-'
    return str(chr(ord('A') + num))

def to_text(token):
    if (token == float('inf')):
        return '\u221e'
    return str(token)
        
def print_compact(m1, m2):
    m = []
    for i in range(len(m1)):
        x = []
        for j in range(len(m1[i])):
            x.append(to_text(m1[i][j]) + to_alphabet(m2[i][j]))
        m.append(x)
    
    mx = 0
    for i in m:
        for j in i:
            mx = max(mx, len(str(j)))
            
    mx += 2


    print('    ', end='')
    print('-'*(2+(mx+2)*(len(m[0]))))

    row_no = 0

    for i in m:
        print(f"  {chr(ord('A') + row_no)} ", end = '')
        row_no += 1

        print('| ', end = '')

        for j in i:
            x = str(j)
            print(' '*(mx - len(x)) + x, end = ' |')
        print()
        print('    ', end = '')
        print('-'*(2+(mx+2)*(len(m[0]))))