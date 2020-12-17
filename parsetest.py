bad_list=[20,22,50,10]
good_list=[20,40,60,80]


def parse_list(parsme):
    good_list = True
    for i in range(0,len(parsme)):
        look_for = parsme[i]
        for x in range(i+1, len(parsme)):
            print('i =',i,' x= ',x)
            print(abs(parsme[i] - parsme[x]))
            if abs((parsme[i] - parsme[x])) < 15:
                good_list = False
    return good_list
    
    
print(parse_list(good_list))
print('--------')
print(parse_list(bad_list))