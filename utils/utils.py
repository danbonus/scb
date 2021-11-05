def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def choice_book(hw):
    book = "📘"
    books_names = {
        "ничего.": "📗",
        "ещё неизвестно.": "📔",
        "неизвестно.": "📕"
    }

    if hw in list(books_names.keys()):
        book = books_names[hw]

    return book
