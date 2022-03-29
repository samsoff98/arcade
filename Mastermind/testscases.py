import introcs
import round
import app4
import models4
import consts



# def compare_guess (code, guess):
#
#     # alist = [3,1,8,6]
#     # blist = [4,6,8,8]
#     result = []
#
#     a=0
#     b=0
#     while a < len(code):
#         while b < len(guess):
#             numA = code[a]
#             numB = guess[b]
#             if numA == numB:
#                 if a ==b:
#                     result.append(1)
#                     code.pop(a)
#                     if a>0:
#                         a-=1
#                     guess.pop(b)
#                     b-=1
#             b+=1
#         b=0
#         a+=1
#
#     a=0
#     b=0
#     while a < len(code):
#         while b < len(guess):
#             numA = code[a]
#             numB = guess[b]
#             if numA == numB:
#                 result.append(2)
#                 code.pop(a)
#                 if a>0:
#                     a-=1
#                 guess.pop(b)
#                 b=0
#                 if b>0:
#                     b-=1
#
#             else:
#                 b+=1
#         b=0
#         a+=1
#     return result


#
#


def compare_guess (code, guess):
    tups = []
    code_pos = 0
    for i in code:
        guess_pos = 0
        for j in guess:
            if i==j:
                t = (code_pos,guess_pos)
                tups.append(t)
            guess_pos +=1
        code_pos +=1

    result = tups_to_final(tups)
    return result

def tups_to_final(tups):
    counted_code = []
    counted_guess = []
    result = []
    for i in tups:
        (a,b) = i
        if a == b:
            counted_code.append(a)
            counted_guess.append(b)
            result.append(1)
    for i in tups:
        (a,b)=i
        if not (a in counted_code or b in counted_guess):
            counted_code.append(a)
            counted_guess.append(b)
            result.append(2)
    return result





#




def test():
    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,4]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess1 = [5,6,4,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2],result1)

    code = [1,2,3,4]
    guess1 = [5,6,3,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,3]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2],result1)

    code = [1,2,3,4]
    guess1 = [5,2,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess1 = [2,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2],result1)

    code = [1,2,3,4]
    guess1 = [1,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess1 = [5,1,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2],result1)

    code = [1,2,3,4]
    guess1 = [5,6,3,4]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1],result1)

    code = [1,2,3,4]
    guess1 = [5,4,3,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)

    code = [1,2,3,4]
    guess1 = [4,6,3,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)

    code = [1,2,3,4]
    guess1 = [1,6,3,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1],result1)

    code = [1,2,3,4]
    guess1 = [1,2,3,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1,1],result1)

    code = [1,2,3,4]
    guess1 = [2,2,2,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [2,2,3,4]
    guess1 = [5,6,2,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2],result1)

    code = [2,2,3,4]
    guess1 = [5,6,2,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2,2],result1)

    code = [2,2,3,4]
    guess1 = [2,6,2,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)

    code = [1,2,2,4]
    guess1 = [2,4,2,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2,2],result1)

    code = [1,2,3,4]
    guess1 = [4,3,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2,2],result1)

    code = [1,2,3,4]
    guess1 = [3,1,2,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2,2,2],result1)

    code = [1,2,3,4]
    guess1 = [3,1,3,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)

    code = [1,2,3,4]
    guess1 = [1,6,1,1]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess1 = [2,2,1,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)

    code = [1,2,3,4]
    guess1 = [4,6,3,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2,2],result1)

    code = [1,2,3,4]
    guess1 = [3,2,1,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2,2],result1)

    code = [1,2,3,4]
    guess1 = [1,2,4,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1,2],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)

    code = [1,2,3,4]
    guess1 = [5,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([],result1)








    code = [1,2,3,4]
    guess2 = [1,5,6,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)



    code = [1,2,3,4]
    guess2 = [1,5,2,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,2],result2)

    code = [1,2,3,4]
    guess1 = [1,5,6,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)

    code = [1,2,3,4]
    guess2 = [1,2,6,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)

    code = [1,2,3,4]
    guess2 = [1,2,4,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1,2],result2)

    code = [2,2,2,2]
    guess1 = [2,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [2,2,2,4]
    guess2 = [1,5,6,2]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2],result2)

    code = [1,2,3,2]
    guess2 = [1,5,2,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,2],result2)

    code = [2,2,3,4]
    guess1 = [2,2,2,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1],result1)

    code = [2,2,2,4]
    guess2 = [2,2,2,2]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1,1],result2)

    code = [2,2,2,4]
    guess2 = [1,2,4,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,2],result2)




    code = [1,2,3,4]
    guess1 = [4,2,7,1]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2,2],result1)



    code = [1,2,3,4]
    guess2 = [4,3,2,1]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2,2,2],result2)

    code = [1,1,3,4]
    guess2 = [4,5,1,1]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2,2],result2)

    code = [1,2,2,2]
    guess1 = [2,1,2,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1,2,2],result1)

    code = [3,2,3,2]
    guess2 = [3,3,3,3]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)

    code = [1,2,2,1]
    guess2 = [2,1,1,2]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2,2,2],result2)

    code = [1,2,3,4]
    guess1 = [5,2,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess2 = [5,6,3,8]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)

    code = [1,2,3,4]
    guess2 = [6,5,7,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)

    code = [1,2,3,4]
    guess1 = [1,2,2,4]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1,1],result1)

    code = [1,2,3,4]
    guess2 = [1,6,7,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)

    code = [1,2,3,4]
    guess2 = [5,2,6,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)










    code = [1,2,3,4]
    guess1 = [1,3,7,3]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2],result1)



    code = [1,2,3,4]
    guess2 = [5,2,6,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)



    code = [1,2,3,4]
    guess2 = [5,5,2,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2],result2)

    code = [1,2,2,5]
    guess1 = [1,5,6,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2,2],result1)

    code = [5,5,5,5]
    guess2 = [5,2,6,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)

    code = [5,5,5,4]
    guess2 = [4,5,5,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1,1],result2)

    code = [1,2,3,4]
    guess1 = [2,6,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2],result1)

    code = [1,2,2,4]
    guess2 = [1,2,6,2]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1,2],result2)

    code = [1,2,3,2]
    guess2 = [3,5,2,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2],result2)

    code = [2,2,3,4]
    guess1 = [4,3,2,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([2,2,2,2],result1)

    code = [1,2,1,4]
    guess2 = [1,1,1,2]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1,2],result2)

    code = [1,2,2,4]
    guess2 = [1,2,4,7]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1,2],result2)




    code = [1,2,3,4]
    guess1 = [4,2,7,1]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,2,2],result1)



    code = [1,2,3,4]
    guess2 = [4,3,2,1]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2,2,2],result2)

    code = [1,1,3,4]
    guess2 = [4,5,1,1]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2,2],result2)

    code = [1,2,2,2]
    guess1 = [2,1,2,2]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1,2,2],result1)

    code = [3,2,3,2]
    guess2 = [3,3,3,3]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)

    code = [1,2,2,1]
    guess2 = [2,1,1,2]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([2,2,2,2],result2)

    code = [1,2,3,4]
    guess1 = [5,2,7,8]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1],result1)

    code = [1,2,3,4]
    guess2 = [5,6,3,8]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)

    code = [1,2,3,4]
    guess2 = [6,5,7,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1],result2)

    code = [1,2,3,4]
    guess1 = [1,2,2,4]
    result1 = compare_guess(code,guess1)
    introcs.assert_equals([1,1,1],result1)

    code = [1,2,3,4]
    guess2 = [1,6,7,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)

    code = [1,2,3,4]
    guess2 = [5,2,6,4]
    result2 = compare_guess(code,guess2)
    introcs.assert_equals([1,1],result2)

print("testing")
test()
print("test complete")





def biglist ():
    biglist = []
    for a in range(8):
        for b in range(8):
            for c in range(8):
                for d in range(8):
                    list = [a,b,c,d]
                    biglist.append(list)

    print(biglist)



def checklist ():
    clist = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    list = [a,b,c,d]
                    clist.append(list)

    print(clist)

#biglist()
checklist()
