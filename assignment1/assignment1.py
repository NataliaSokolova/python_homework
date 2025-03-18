# Write your code here.
def hello():
    return "Hello!"

def greet(name):
    return ("Hello, " + name + "!")
   
def calc(a,b,c = "multiply"):
    try:
        if c == "add":
            return a + b
        elif c == "subtract":
            return a - b
        elif c == "multiply":
            return a * b
        elif c ==  "divide":
            return a/b
        elif c ==  "modulo":
            return a % b
        elif c ==  "int_divide":
           return a // b
        elif c ==  "power":
            return a ** b
        else:
           return "Invalid operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
        
def data_type_conversion(a,b):
    try:    
        if b == "float":
            return float(a)
        elif b == "str":
            return str(a)
        elif b == "int":
            return int(a)
        else:
            return "Invalid data type requested"

    except (ValueError, TypeError):
            return f"You can't convert {a} into a {b}."
def grade(*args):
    try:
        avarage = sum(args) / len(args)
        if avarage >= 90:
            return "A"
        elif avarage >= 80:
            return "B"
        elif avarage >= 70:
            return "C"
        elif avarage >=60:
            return "D"
        else:
            return "F"
    except (TypeError, ValueError, ZeroDivisionError):
            return "Invalid data was provided."
    
def repeat(string: str, count: int):   
    result  = ""
    for _ in range (count):
        result += string
    return result    

def student_scores(mode, **kwargs):
    if mode == "best":
        if not kwargs:
            return "No scores provided"
        best_student = max(kwargs, key = kwargs.get)
        return best_student   
    elif mode == "mean":
        if not kwargs:
            return "No scores provided."
        mean_score = sum(kwargs.values()) /len (kwargs)
        return mean_score
    else:
        return "Invalid mode. Please use 'best' or 'mean'."
    
    # Task 8: Titleize, with String and List Operations

    
def titleize(string: str) -> str:
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = string.split()
    for i, word in enumerate(words):
        if i == 0 or i == len(words) -1:
            words[i] = word.capitalize()
        elif word.lower() not in little_words:
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()
    return " ".join(words)   


# Task 9: Hangman, with more String Operations
def hangman(secret: str, guess: str) -> str:
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result +=  "_"
    return result                   

#Task 10: Pig Latin, Another String Manipulation Exercise


def pig_latin(string: str) -> str:
    vowels = {"a", "e", "i", "o", "u"}
    result = []

    for word in string.split():
        if word[0] in vowels:
            result.append(word + "ay")
        else:
            if "qu" in word:
                qu_index = word.find("qu")
                result.append(word[qu_index + 2:] + word[:qu_index + 2] + "ay")
            else:
                consonant_cluster = ""
                i = 0
                while i < len(word) and word[i] not in vowels:
                  consonant_cluster += word[i]
                  i += 1  
                result.append(word[i:] + consonant_cluster + "ay")    
    return " ".join(result)            



    









