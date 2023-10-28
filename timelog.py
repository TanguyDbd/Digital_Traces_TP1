import collections
import logging
import time

# Decorator to measure execution time 
def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # Log the execution time
        logging.info(f'{func.__name__} took {execution_time} seconds to execute.')
        return result, execution_time
    return wrapper

def count_words_with_dict(text):
    words = text.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def count_words_with_counter(text):
    words = text.split()
    word_count = collections.Counter(words)
    return word_count

@execution_time_decorator
def count_dict(text):
    return count_words_with_dict(text)
        
@execution_time_decorator
def count_counter(text):
    return count_words_with_counter(text)