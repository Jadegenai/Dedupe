keyboard_dict = {
    '1': {'row': 'top', 'finger': 'left pinky'},
    '2': {'row': 'top', 'finger': 'left ring'},
    '3': {'row': 'top', 'finger': 'left middle'},
    '4': {'row': 'top', 'finger': 'left index'},
    '5': {'row': 'top', 'finger': 'left index'},
    '6': {'row': 'top', 'finger': 'right index'},
    '7': {'row': 'top', 'finger': 'right index'},
    '8': {'row': 'top', 'finger': 'right middle'},
    '9': {'row': 'top', 'finger': 'right ring'},
    '0': {'row': 'top', 'finger': 'right pinky'},
    '!': {'row': 'top', 'finger': 'left pinky'},
    '@': {'row': 'top', 'finger': 'left ring'},
    '#': {'row': 'top', 'finger': 'left middle'},
    '$': {'row': 'top', 'finger': 'left index'},
    '%': {'row': 'top', 'finger': 'left index'},
    '^': {'row': 'top', 'finger': 'right index'},
    '&': {'row': 'top', 'finger': 'right index'},
    '*': {'row': 'top', 'finger': 'right middle'},
    '(': {'row': 'top', 'finger': 'right ring'},
    ')': {'row': 'top', 'finger': 'right pinky'},
    '-': {'row': 'top', 'finger': 'right pinky'},
    '=': {'row': 'top', 'finger': 'right pinky'},
    '_': {'row': 'top', 'finger': 'right pinky'},
    '+': {'row': 'top', 'finger': 'right pinky'},
    'q': {'row': 'home', 'finger': 'left pinky'},
    'w': {'row': 'home', 'finger': 'left ring'},
    'e': {'row': 'home', 'finger': 'left middle'},
    'r': {'row': 'home', 'finger': 'left index'},
    't': {'row': 'home', 'finger': 'left index'},
    'y': {'row': 'home', 'finger': 'right index'},
    'u': {'row': 'home', 'finger': 'right index'},
    'i': {'row': 'home', 'finger': 'right middle'},
    'o': {'row': 'home', 'finger': 'right ring'},
    'p': {'row': 'home', 'finger': 'right pinky'},
    '[': {'row': 'home', 'finger': 'right pinky'},
    ']': {'row': 'home', 'finger': 'right pinky'},
    '{': {'row': 'home', 'finger': 'right pinky'},
    '}': {'row': 'home', 'finger': 'right pinky'},
    '\\': {'row': 'home', 'finger': 'right pinky'},
    '|': {'row': 'home', 'finger': 'right pinky'},
    'a': {'row': 'bottom', 'finger': 'left pinky'},
    's': {'row': 'bottom', 'finger': 'left ring'},
    'd': {'row': 'bottom', 'finger': 'left middle'},
    'f': {'row': 'bottom', 'finger': 'left index'},
    'g': {'row': 'bottom', 'finger': 'left index'},
    'h': {'row': 'bottom', 'finger': 'right index'},
    'j': {'row': 'bottom', 'finger': 'right index'},
    'k': {'row': 'bottom', 'finger': 'right middle'},
    'l': {'row': 'bottom', 'finger': 'right ring'},
    ';': {'row': 'bottom', 'finger': 'right pinky'},
    '\'': {'row': 'bottom', 'finger': 'right pinky'},
    ':': {'row': 'bottom', 'finger': 'right pinky'},
    '"': {'row': 'bottom', 'finger': 'right pinky'},
    'z': {'row': 'bottom', 'finger': 'left pinky'},
    'x': {'row': 'bottom', 'finger': 'left ring'},
    'c': {'row': 'bottom', 'finger': 'left middle'},
    'v': {'row': 'bottom', 'finger': 'left index'},
    'b': {'row': 'bottom', 'finger': 'left index'},
    'n': {'row': 'bottom', 'finger': 'right index'},
    'm': {'row': 'bottom', 'finger': 'right index'},
    ',': {'row': 'bottom', 'finger': 'right middle'},
    '.': {'row': 'bottom', 'finger': 'right ring'},
    '/': {'row': 'bottom', 'finger': 'right pinky'},
    '<': {'row': 'bottom', 'finger': 'right middle'},
    '>': {'row': 'bottom', 'finger': 'right ring'},
    '?': {'row': 'bottom', 'finger': 'right pinky'},
    ' ': {'row': 'down-2', 'finger': 'thumb'}
}

keypad_dict = {
    '7': {'row': 'up-1', 'finger': 'right pointer'},
    '8': {'row': 'up-1', 'finger': 'right middle'},
    '9': {'row': 'up-1', 'finger': 'right ring'},
    '4': {'row': 'home', 'finger': 'right pointer'},
    '5': {'row': 'home', 'finger': 'right middle'},
    '6': {'row': 'home', 'finger': 'right ring'},
    '+': {'row': 'home', 'finger': 'right pinky'},
    '1': {'row': 'down-1', 'finger': 'right pointer'},
    '2': {'row': 'down-1', 'finger': 'right middle'},
    '3': {'row': 'down-1', 'finger': 'right ring'},
    '0': {'row': 'down-2', 'finger': 'right pointer'},
    '0': {'row': 'down-2', 'finger': 'right middle'},
    '0': {'row': 'down-2', 'finger': 'right thumb'},
    '.': {'row': 'down-2', 'finger': 'right ring'}
}

def levenshtein_distance(s1, s2):
    lenstr1 = len(s1) + 1
    lenstr2 = len(s2) + 1
    # Create a matrix
    matrix = [[0 for n in range(lenstr2)] for m in range(lenstr1)]
    for i in range(lenstr1):
        matrix[i][0] = i
    for j in range(lenstr2):
        matrix[0][j] = j
    for i in range(1, lenstr1):
        for j in range(1, lenstr2):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i-1][j] + 1,      # deletion
                                matrix[i][j-1] + 1,      # insertion
                                matrix[i-1][j-1] + cost) # substitution
    return matrix[lenstr1 - 1][lenstr2 - 1]

def typo_measurement(s1, s2):
    lenstr1 = len(s1) + 1
    lenstr2 = len(s2) + 1
    # Create a matrix
    matrix = [[0 for n in range(lenstr2)] for m in range(lenstr1)]
    for i in range(lenstr1):
        matrix[i][0] = i * 5

    for j in range(lenstr2):
        matrix[0][j] = j * 1

    for i in range(1, lenstr1):
        for j in range(1, lenstr2):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                l1 = s1[i-1].lower()
                l2 = s2[j-1].lower()
                if keyboard_dict[l1]["finger"] == keyboard_dict[l2]["finger"]:
                    cost = 1
                elif keyboard_dict[l1]["row"] == keyboard_dict[l2]["row"]:
                    cost = 3
                else:
                    cost = 6
            matrix[i][j] = min(matrix[i-1][j] + matrix[i][j-1], # zero explanation substitution
                            matrix[i-1][j-1] + cost,
                            matrix[i][j-1] + 1
                            ) # substitution
    return matrix[lenstr1 - 1][lenstr2 - 1]

def either_way_typo_measurement(s1,s2):
    return min(
        typo_measurement(s1,s2),
        typo_measurement(s2,s1)
    )

def quick_typo_check(s1,s2):
    return len(set(s1).difference(s2)) < 4