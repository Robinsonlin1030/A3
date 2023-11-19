"""CSC108: Fall 2023 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of students taking
CSC108 at the University of Toronto. Copying for purposes other than this use is
expressly prohibited. All forms of distribution of this code, whether as given 
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Anya Tafliovich, Michelle Craig, Tom Fairgrieve, Sadia
Sharmin, and Jacqueline Smith.
"""

from typing import Union

ID = 'identifier'
TITLE = 'title'
CREATED = 'created'
MODIFIED = 'modified'
AUTHORS = 'authors'
ABSTRACT = 'abstract'
END = 'END'

# We store names as tuples of two strs: (last-name, first-name(s)).
NameType = tuple[str, str]

# ArticleValueType is the type for valid values in the ArticleType
# dict.  All values are str, except for the value associated with
# key AUTHORS, which is a list of NameType.
# Note that we have not taught you Union - you can read it as "or"
ArticleValueType = Union[str, list[NameType]]

# ArticleType is a dict that maps keys ID, TITLE, CREATED, MODIFIED,
# AUTHORS, and ABSTRACT to their values (of type ArticleValueType).
ArticleType = dict[str, ArticleValueType]

# ArxivType is a dict that maps article identifiers to articles,
# i.e. to values of type ArticleType.
ArxivType = dict[str, ArticleType]
