import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def square(vec):
    value = 0
    for i in vec:
        value += i**2

    return value


def cosine_similarity(vec1, vec2):
    #Find the keys that are the same in both,
    #Find the values at those keys
    #Implement the formula on page 1

    vec1_keys = list(vec1.keys())
    vec2_keys = list(vec2.keys())
    vec1_num = list(vec1.values())
    vec2_num = list(vec2.values())


    vec1_values = []
    vec2_values = []
    numerator = 0

    if len(vec1) >= len(vec2):
        for i in range(len(vec1_keys)):
            if vec1_keys[i] in vec2_keys:
                vec1_values.append(vec1[vec1_keys[i]])
                vec2_values.append(vec2[vec1_keys[i]])

    else:
        for i in range(len(vec2_keys)):
            if vec2_keys[i] in vec1_keys:
                vec1_values.append(vec1[vec2_keys[i]])
                vec2_values.append(vec2[vec2_keys[i]])

    for j in range(len(vec1_values)):
        numerator += (vec1_values[j] * vec2_values[j])

    square1 = square(vec1_num)
    square2 = square(vec2_num)


    similarity = (numerator)/((math.sqrt(square1*square2)))


    return similarity


def deep_copy(obj):
    '''Return a deep (i.e., non-aliased at all) copy of obj, a nested list of
    integers'''
    #Base case:
    if type(obj) != list:
        return obj
    copy = []
    for elem in obj:
        #The leap of faith: assume that deep_copy works!
        copy.append(deep_copy(elem))
    return copy


def build_semantic_descriptors(sentences):
    ''' FIX THIS: words that appear multiple times in a sentence do not count'''
    #given a list of sentences
    #create a dictionary for every word and the values are the other words in the same sentences
    semantic = {}
    values= {}
    words = 0


    for i in range(len(sentences)):
        d = list(sentences[i])
        d = [x.lower() for x in d]
        d = set(d)
        for j in d:

            if j in semantic:
                for k in d:
                    if j != k:

                        if k in semantic[j]:
                            semantic[j][k] += 1
                        else:
                            semantic[j][k] = 1

            else:
                values = {}
                for k in d:
                    if k != j:
                        if k not in values:

                            values[k] = values.get(k,0) +1
                            semantic[j] = values



    return semantic







def build_semantic_descriptors_from_files(filenames):
    punctuation =[",",".","-","--",":",";","?","!"]
    sentences = []

    for i in range(len(filenames)):
        sentence = []
        f = open(filenames[i],"r",encoding = "latin1")
        text = f.read()

        for j in punctuation:

            if j in [".","!","?"]:
                text = text.replace(j,"!")


            elif j in [",","-","--",":",";"]:
                text = text.replace(j," ")


        text = text.replace("\n"," ")
        text = text[:len(text)-1]
        text = text.split("! ")


        for i in text:

            text = i.strip("!").split()
            sentences.append(text)



    return build_semantic_descriptors(sentences)








def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    #Find the word in the dictionary "key"
    #get values for that key
    #use cosine similarity
    #return higher one
    similarity = []
    word_values = semantic_descriptors.get(word)
    if word_values != None: #added this


        for i in choices:
            value = semantic_descriptors.get(i)
            if value != None:
                similarity.append(similarity_fn(word_values,value))
            else:
                similarity.append(-1)

        final_max = -1
        first_max = -1
        for i in range(len(similarity)):
            first_max = similarity[i]
            final_max = max(first_max,final_max)

        ind = similarity.index(final_max)

    else:
        ind = 0 #added this

    return choices[ind]




def run_similarity_test(filename, semantic_descriptors, similarity_fn):
        f = open(filename,"r",encoding = "latin1")
        text = f.read()

        text = text.split("\n")

        counter = 0
        text_length = len(text)
        for i in range(len(text)):
            if text[i] != "":

                line = text[i]
                line = line.split(" ")

                word =line[0]
                correct_answer = line[1]
                choices = line[2:]

                guess = most_similar_word(word,choices,semantic_descriptors,similarity_fn)

                if guess == correct_answer:
                    counter += 1
            else:
                text_length -= 1

        percentage = (counter/(text_length)) *100

        return percentage






if __name__ == "__main__":
    #print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6,"a":2}))
    sentences = [["i", "Am", "A", "sick", "man","i","i"],
["I", "am", "a", "spiteful", "man"]]
# ["i", "am", "an", "unattractive", "man"],["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    #print(build_semantic_descriptors(sentences))
    sem_desc = build_semantic_descriptors_from_files(["text2.txt","text1.txt"])
    #sem_desc = {"dog": {"cat": 1, "food": 1},"cat": {"dog": 1,}}
    #print(most_similar_word("bat",["cat","rat"],sem_desc,cosine_similarity))
    print(run_similarity_test("test.txt",sem_desc,cosine_similarity))
