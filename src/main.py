def check_integers(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        words = result.split()
        shortened_words = []
        for word in words:
            if len(word) > 8:
                shortened_word = word[:8] + "."
                shortened_words.append(shortened_word)
            else shortened_words.append(word)
        return " ".join(shortened_words)

    return wrapper