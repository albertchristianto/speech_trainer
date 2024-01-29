def remove_space_before_after_text(text):
    if text=="":
        return ""
    #before
    idx = -1
    for i, each in enumerate(text):
        if each != ' ':
            break
        idx = i
    if idx !=-1:
        text = text[(idx + 1):]
    if text=="":
        return ""
    #after
    have_space = False
    idx = len(text) - 1
    while True:
        if text[idx] != ' ':
            break
        have_space = True
        idx -= 1
    if have_space:
        text = text[:(idx+1)]

    return text