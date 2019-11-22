"""
Programming task
================
The following is an implementation of a simple Named Entity Recognition (NER).
NER is concerned with identifying place names, people names or other special
identifiers in text.
Here we make a very simple definition of a named entity: A sequence of
at least two consecutive capitalized words. E.g. "Los Angeles" is a named
entity, "our hotel" is not.
While the implementation passes the Unit test, it suffers from bad structure and
readability. It is your task to rework *both* the implementation and the Unit
test. You are expected to come up with a better interface than the one presented
here.
Your code will be evaluated on:
- Readability: Is naming intuitive? Are there comments where necessary?
- Structure: Is functionality grouped into functions or classes in a way that
enables reusability?
- Testability: Is it easy to test individual components of your algorithm? This
is a good indicator of good interface design.
- Bonus: Functional programming. Demonstrate how you have applied principles of
functional programming to improve this code.
If you want, explain reasons for changes you've made in comments.
Note that you don't have to improve the actual Named Entity Recognition
algorithm itself - the focus is on code quality.
"""

import re
import unittest

"""
Code Modifications
==================
My code splits functionality into the operations tokenize(text) and
named_entities(tokens).
I changed token_re to match only the token itself, rather than capturing the
whole rest of the string in the second group. This way, my tokenize function
can use lazy evaluation on the text and works better on longer input.
"""

# Regular expression for matching a token at the beginning of a sentence
token_re = re.compile(r"([a-z]+)\s*", re.I)
# Regular expression to recognize an uppercase token
uppercase_re = re.compile(r"[A-Z][a-z]*$")

def tokenize(text, token_re=token_re):
	"""
	Returns a generator for tokens in the given text.
	"""
	return (match.group(1) for match in token_re.finditer(text))

def named_entities(
		tokens,
		is_entity_part=(lambda token: uppercase_re.match(token)),
		min_repetitions=2):
	"""
	Extracts all named entities from the given token collection.
	Named entities may span multiple tokens.
	
	@param tokens: iterator over tokens
	@param is_entity_part: function which takes a token and returns bool
	@param min_repetitions: named entities consist of at least this many tokens
	@return: a set of the named entities in the token list
	"""
	entities = set()
	current_entity = []
	for token in tokens:
		if is_entity_part(token):
			current_entity.append(token)
		else:
			if len(current_entity) >= min_repetitions:
				entities.add(' '.join(current_entity))
			current_entity = []
	if len(current_entity) >= min_repetitions:
		entities.add(' '.join(current_entity))
	return entities


class NamedEntityTestCase(unittest.TestCase):

	def test_ner_extraction(self):
		text = "When we went to Los Angeles last year we visited the Hollywood Sign"
		self.assertEqual(set(["Los Angeles", "Hollywood Sign"]),
				named_entities(tokenize(text)))

if __name__ == "__main__":
    unittest.main()
