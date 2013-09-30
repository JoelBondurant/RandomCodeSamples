import re

class Highlighter:
    """
    A class to bundle up Yelp text snippit summarization for interview homework.
    """


    def __init__(self, doc, query, minimum_snippit_length=30, maximum_snippit_length=160):
        """ Constructor with Highlighter defaults. """
        self.doc = doc
        self.query = query
        self.minimum_snippit_length = minimum_snippit_length
        self.maximum_snippit_length = maximum_snippit_length
        self.doc_length = len(doc)
        self.query_terms = None
        self.num_query_terms = None


    def tokenize_query_terms(self):
        """
        Returns:
            query_terms - The word tokens of the query. (list(str))
        """
        query_terms_orig = re.split(r'\W', self.query)
        query_terms = []
        for query_term in query_terms_orig:
            if query_term: # skip empty query tokens (e.g. punctuation)
                query_terms.append(query_term)
        self.query_terms = query_terms
        self.num_query_terms = len(query_terms)
        return self.query_terms


    def locate_query_term_starts(self, query_term):
        """
        Args:
            query_term - A word token from a query string. (str)
        Returns:
            A list of the start locations in increasing order of the query word token. (list(str))
        """
        return [m.start() for m in re.finditer(query_term, self.doc)]


    def query_term_partial_density(self):
        """
        Args:
            query_terms - A list of the query terms / word tokens. (list(str))
        Returns:
            A discrete partial density function of query terms to model query term
            density on a character basis rather than word blocks.
            I'm weighting each term locally, so don't expect these to be normalized
            probability distributions over characters. The algorithm could be 
            configured with other weighting, to reduce the scoring of repeated term
            occurence.
            The result is a 2D list where the primary index is on query_term index, 
            and the second index is on character number in document. - (list(list(float)))
        """
        partial_term_density = [None] * self.num_query_terms
        for query_term_index in range(0, self.num_query_terms):
            partial_term_density[query_term_index] = [0] * self.doc_length
            query_term = self.query_terms[query_term_index]
            query_term_length = len(query_term)
            query_term_starts = self.locate_query_term_starts(query_term)
            for query_term_start in query_term_starts:
                for doc_char_index in range(query_term_start, query_term_start + query_term_length):
                    partial_term_density[query_term_index][doc_char_index] = 1.0 / query_term_length
        return partial_term_density


    def query_term_density(self, partial_term_density):
        """
        Args:
            partial_term_density - The output of self.query_term_partial_density. (list(list(float)))
        Returns:
            A discrete (non-normalized) density of query word tokens in the document. (list(float))
        """
        total_density = [0] * self.doc_length # initalize, assuming non-empty
        for query_term_index in range(0, self.num_query_terms):
            for dci in range(0, self.doc_length): # dci: document_character_index
                total_density[dci] = total_density[dci] + partial_term_density[query_term_index][dci]
        return total_density


    def locate_maxima(self, a_list):
        """
        Args:
            a_list - A list of numbers. (number)
        Returns:
            A list of position(s) in the list of the maxima. (list(int))
        """
        max_a_list = max(a_list)
        return [i for i, j in enumerate(a_list) if j == max_a_list]


    def max_term_density_window(self, total_density):
        """
        Args:
            total_density - A discrete density of query terms in the document. (list(float))
        Returns:
            A single framed window over the document which seeks to maximize the query
            term density with minimal size. Lots of things could be done in here with 
            weighting tweaks (e.g. don't count repeat terms as much), and optimization
            (e.g. I think there is much redundant summation going on here, and I'm not 
            making use of parallelism with something like PyOpenCL.)  (list(int))
        """
        scores = []
        # starting by taking the maximum window size for the snippit, sliding it across the doc
        # scoring the position by summing over the term densities.
        window = [0, self.maximum_snippit_length]
        while True:
            score = sum(total_density[window[0]:window[1]]) # score ~ density integration
            scores.append(score)
            if (window[1] >= self.doc_length):
                break
            else:
                window[0] = window[0] + 1
                window[1] = window[1] + 1
        max_score = max(scores)
        max_score_locations_orig = self.locate_maxima(scores)
        max_score_offset = self.maximum_snippit_length // 2 # estimate the max density at the window midpoint.
        max_score_locations = [(element + max_score_offset) for element in max_score_locations_orig]
        # now that we have estimates for the query term maximal density zones,
        # we can refine the windows around those estimates.
        subwindow_steps = []
        for max_score_location in max_score_locations:
            step = self.minimum_snippit_length // 2
            while True:
                subwindow = [max_score_location - step, max_score_location + step]
                score = sum(total_density[subwindow[0]:subwindow[1]])
                if (subwindow[0] <= 0 or subwindow[1] >= self.doc_length or score >= max_score):
                    break
                else:
                    step = step + 1
            subwindow_steps.append(step)
        min_subwindow_steps = min(subwindow_steps)
        optimal_subwindow_index = subwindow_steps.index(min_subwindow_steps)
        max_score_location = max_score_locations[optimal_subwindow_index]
        optimal_subwindow = [max_score_location - min_subwindow_steps, max_score_location + min_subwindow_steps]
        return optimal_subwindow


    def highlight(self, snippit):
        """
        Args:
            snippit - The raw text snippit. (str)
        Returns:
            The text snippit with query terms highlighted. (str)
        """
        if (self.query_terms is None):
            return snippit
        hsnippit = snippit
        hlt = "[[HIGHLIGHT]]"
        hlt_regex = r"\[\[HIGHLIGHT\]\]"
        for query_term in self.query_terms:
            hsnippit = re.sub(query_term, hlt + query_term + hlt, hsnippit)
        hsnippit = re.sub(hlt_regex + r"\W{0,4}"  +  hlt_regex, " ", hsnippit)
        return hsnippit


    def highlight_document(self):
        """
        Returns:
            The most relevant snippet with the query terms highlighted (str)
        """
        if len(self.doc) <= self.maximum_snippit_length:
            return self.highlight(self.doc) # For short documents, just return the whole thing quickly.
        if self.query is None or len(self.query) <= 1:
            return self.highlight(self.doc[0:self.maximum_snippit_length])
        self.tokenize_query_terms()
        query_term_partial_density = self.query_term_partial_density()
        total_query_term_density = self.query_term_density(query_term_partial_density)
        max_term_density_window = self.max_term_density_window(total_query_term_density)
        optimal_snippit = self.doc[max_term_density_window[0]:max_term_density_window[1]]
        return self.highlight(optimal_snippit)


    @staticmethod
    def highlight_doc(doc, query):
        """
        Args:$
            doc - Document to be highlighted (str)$
            query - The search query (str)$
        Returns:
            A document summary snippit with query terms highlighted. (str)
        """
        hilite = Highlighter(doc, query)
        return hilite.highlight_document()

