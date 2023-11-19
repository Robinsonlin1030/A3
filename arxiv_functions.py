"""CSC108: Fall 2023 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of students taking
CSC108 at the University of Toronto. Copying for purposes other than this use is
expressly prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Anya Tafliovich, Michelle Craig, Tom Fairgrieve, Sadia
Sharmin, and Jacqueline Smith.
"""

import copy  # needed in examples of functions that modify input dict
from typing import TextIO, Tuple

from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS, ABSTRACT, END,
                       NameType, ArticleValueType, ArticleType, ArxivType)


################################################################################
# Sample data for use in docstring examples
################################################################################
EXAMPLE_ARXIV = {
    '5090': {
        ID: '5090',
        TITLE: "Increasing Students' Engagement to Reminder Emails",
        CREATED: '',
        MODIFIED: '2022-08-02',
        AUTHORS: [('Yanez', 'Fernando'), ('Zavaleta-Bernuy', 'Angela')],
        ABSTRACT: 'Our metric of interest is open email rates.'},
    '03221': {
        ID: '03221',
        TITLE: 'Stargazer: An Interactive Camera Robot for How-To Videos',
        CREATED: '2023-03-01',
        MODIFIED: '2023-03-06',
        AUTHORS: [('Grossman', 'Tovi')],
        ABSTRACT: ('We present Stargazer, a novel approach for assisting ' +
                   'with tutorial content creation.')},
    '0001': {
        ID: '0001',
        TITLE: 'Cats and Dogs Can Co-Exist',
        CREATED: '2023-08-20',
        MODIFIED: '2023-10-02',
        AUTHORS: [('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia')],
        ABSTRACT: 'We show a formal proof that cats and dogs\n' +
        'can peacefully co-exist!'},
    '108': {
        ID: '108',
        TITLE: 'CSC108 is the Best Course Ever',
        CREATED: '2023-09-01',
        MODIFIED: '',
        AUTHORS: [('Smith', 'Jacqueline E.'), ('Zavaleta-Bernuy', 'Angela'),
                  ('Campbell', 'Jen')],
        ABSTRACT: 'We present clear evidence that Introduction to\n'
        + 'Computer Programming is the best course'},
    '42': {
        ID: '42',
        TITLE: '',
        CREATED: '2023-05-04',
        MODIFIED: '2023-05-05',
        AUTHORS: [],
        ABSTRACT: 'This is a strange article with no title\n'
        + 'and no authors.\n\nIt also has a blank line in its abstract!'}
}

EXAMPLE_BY_AUTHOR = {
    ('Campbell', 'Jen'): ['108'],
    ('Grossman', 'Tovi'): ['03221'],
    ('Sharmin', 'Sadia'): ['0001'],
    ('Smith', 'Jacqueline E.'): ['0001', '108'],
    ('Yanez', 'Fernando'): ['5090'],
    ('Zavaleta-Bernuy', 'Angela'): ['108', '5090']
}


################################################################################
# Helper function to use in your code later on.  Do not change these functions.
################################################################################
def clean_word(word: str) -> str:
    """Return word with all non-alphabetic characters removed and converted to
    lowercase.

    Precondition: word contains no whitespace

    >>> clean_word('Hello!!!')
    'hello'
    >>> clean_word('12cat.dog?')
    'catdog'
    >>> clean_word("DON'T")
    'dont'
    """
    new_word = ''
    for ch in word:
        if ch.isalpha():
            new_word = new_word + ch.lower()
    return new_word


################################################################################
# Task 1 - Working with ArxivType
################################################################################
def created_in_year(data: ArxivType, id: str, year: int) -> bool:
    """Determines whether an article in data identified by id was created in
    year.
    >>> created_in_year(EXAMPLE_ARXIV, '0001', 2023)
    True
    >>> created_in_year(EXAMPLE_ARXIV, '108', 2022)
    False
    """
    if id not in data:
        return False
    else:
        if str(year) not in data[id][CREATED]:
            return False
    return True


def contains_keyword(arxiv_data: ArxivType, keyword: str) -> list[str]:
    """
    Return a list of the IDs of articles of arxiv_data that contain the given
    keyword in their title, author names, and/or abstract. The list should be
    sorted in lexicographic order.
    >>> contains_keyword(EXAMPLE_ARXIV, 'cat')
    ['0001']
    >>> contains_keyword(EXAMPLE_ARXIV, 'engagement')
    ['5090']
    """
    matching_ids = []
    keyword = clean_word(keyword)  # Clean the keyword first

    for article_id, article_info in arxiv_data.items():
        title = clean_word(article_info[TITLE])
        abstract = clean_word(article_info[ABSTRACT])
        authors = ' '.join(
            [' '.join(author) for author in article_info[AUTHORS]])
        authors = clean_word(authors)

        if keyword in title.split() or keyword in abstract.split() or \
                keyword in authors.split():
            matching_ids.append(article_id)

    return sorted(matching_ids)


def average_author_count(arxiv_data: ArxivType) -> float:
    """
    Return the average number of authors per article in the arxiv metadata.

    >>> average_author_count(EXAMPLE_ARXIV)
    1.6
    >>> average_author_count({})
    0.0
    """
    total_authors = 0
    total_articles = len(arxiv_data)

    if total_articles == 0:
        return 0.0

    for article_id, article_info in arxiv_data.items():
        total_authors += len(article_info[AUTHORS])

    return total_authors / total_articles


################################################################################
# Task 2 - Reading in the arxiv metadata
################################################################################
def read_arxiv_file(f: TextIO) -> ArxivType:
    """Return a ArxivType dictionary containing the arxiv metadata in f.

    Note we do not include example calls for functions that take open files.
    """
    arxiv_data = {}
    current_article = {ID: '', TITLE: '', CREATED: '', MODIFIED: '',
                       AUTHORS: [], ABSTRACT: ''}
    in_abstract = False

    for line in f:
        line = line.strip()

        if line == END:
            arxiv_data[current_article[ID]] = current_article
            current_article = {ID: '', TITLE: '', CREATED: '', MODIFIED: '',
                               AUTHORS: [], ABSTRACT: ''}
            in_abstract = False
        elif not current_article[ID]:
            current_article[ID] = line
        elif not current_article[TITLE]:
            current_article[TITLE] = line
        elif not current_article[CREATED]:
            current_article[CREATED] = line
        elif not current_article[MODIFIED]:
            current_article[MODIFIED] = line
        elif line and not in_abstract:
            current_article[AUTHORS].append(parse_author(line))
        elif not line:
            in_abstract = True
        else:
            current_article[ABSTRACT] += (line + '\n')

    return arxiv_data


def parse_author(line: str) -> Tuple[str, str]:
    """
    Parse an author's name from a line.

    >>> parse_author("Smith,John")
    ('John', 'Smith')
    >>> parse_author("Ralph,Wang")
    ('Ralph', 'Wang')
    """
    last_name, first_name = line.split(',', 1)
    return first_name.strip(), last_name.strip()


################################################################################
# Task 3 - Working with Authors and Coauthors
################################################################################
def make_author_to_articles(id_to_article: ArxivType
                            ) -> dict[NameType, list[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> make_author_to_articles({})
    {}
    """
    # We have provided the docstring for this function as an example of how
    # to compare dictionaries in a docstring example
    author_to_articles = {}

    for article_id, article_info in id_to_article.items():
        for author in article_info[AUTHORS]:
            if author not in author_to_articles:
                author_to_articles[author] = []
            author_to_articles[author].append(article_id)

    for articles in author_to_articles.values():
        articles.sort()

    return author_to_articles


def get_coauthors(arxiv_data: ArxivType, author: NameType) -> list[NameType]:
    """Return a list of coauthors of the specified author, sorted in
    lexicographic order.
    >>> get_coauthors(EXAMPLE_ARXIV, ('Smith', 'Jacqueline E.'))
    [('Campbell', 'Jen'), ('Sharmin', 'Sadia'), ('Zavaleta-Bernuy', 'Angela')]
    >>> get_coauthors(EXAMPLE_ARXIV, ('Robin', 'Lin'))
    []
    """
    coauthors = set()

    for article_info in arxiv_data.values():
        if author in article_info[AUTHORS]:
            for coauthor in article_info[AUTHORS]:
                if coauthor != author:
                    coauthors.add(coauthor)

    return sorted(list(coauthors))






################################################################################
# Task 4 - Prolific Authors
################################################################################
def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update id_to_article so that it contains only articles published by
    authors with min_publications or more articles published. As long
    as at least one of the authors has min_publications, the article
    is kept.

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    """
    # We have provided you with this docstring as an example of how to use
    # the function copy.deepcopy in docstring examples for functions that
    # modify an argument.

    # TODO write the body of the function here


# TODO write the rest of your Task 4 functions here


if __name__ == '__main__':
    pass
    # uncomment the lines below to run doctest on your code
    # note that doctest requires your docstring examples to be perfectly
    # formatted, and we will not be running doctest on your code
    # import doctest
    # doctest.testmod()

    # uncomment the lines below to work with the small data set
    #example_data = open('example_data.txt')
    #example_arxiv = read_arxiv_file(example_data)
    #example_data.close()
    #if example_arxiv == EXAMPLE_ARXIV:
        #print('The result from your read_arxiv_file matches EXAMPLE_ARXIV!')
        #print('This is a good sign, but do more of your own testing!')
    #else:
        #print('Not quite! You got')
        #print(example_arxiv)
        #print()
        #print('If you are getting this message, then the dictionary produced')
        #print('by your read_arxiv_file function does not match the provided')
        #print('EXAMPLE_ARXIV. Scroll up to see the dictionary your function')
        #print('produced. You should write additional testing code to help')
        #print('figure out why it does not match. You can also try setting a')
        #print('breakpoint on the first line of read_arxiv_file and running')
        #print('the debugger.')

    # uncomment the lines below to work with a larger data set
    #data = open('data.txt')
    #arxiv = read_arxiv_file(data)
    #data.close()

    #author_to_articles = make_author_to_articles(arxiv)
    #most_published = get_most_published_authors(arxiv)
    #print(most_published)
    #print(get_coauthors(arxiv, ('Varanasi', 'Mahesh K.')))  # one
    #print(get_coauthors(arxiv, ('Chablat', 'Damien')))  # many
