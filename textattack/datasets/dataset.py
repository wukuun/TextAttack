from textattack.shared import utils
import pickle

class TextAttackDataset:
    """
    A dataset for text attacks.
    
    Any iterable of (label, text_input) pairs qualifies as 
    a TextAttackDataset.
    
    """
    def __init__(self):
        """ Loads a full dataset from disk. """
        raise NotImplementedError()
    
    def __iter__(self):
        return self
    
    def _process_example(self, raw_line):
        """ Processes each example read from a file. Implemented on a dataset-
            by-dataset basis.
            
            Args:
                raw_line (str): Line of the example to process.
                
            Returns:
                A tuple of text objects
        """
        raise NotImplementedError()
    
    def __next__(self):
        if self.i >= len(self.examples):
            raise StopIteration
        example = self.examples[self.i]
        self.i += 1
        return example
    
    def _load_pickle_file(self, file_name, offset=0):
        self.i = 0
        file_path = utils.download_if_needed(file_name)
        self.examples = pickle.load( open(file_path, "rb" ) )
        self.examples = self.examples[offset:]
    
    def _load_classification_text_file(self, text_file_name, offset=0):
        """ Loads tuples from lines of a classification text file. 
        
            Format must look like:
            
                1 this is a great little ...
                0 "i love hot n juicy .  ...
                0 "\""this world needs a ...
            
            Arguments:
                n (int): number of samples to return
                offset (int): line to start reading from
        """
        text_file_path = utils.download_if_needed(text_file_name)
        text_file = open(text_file_path, 'r')
        raw_lines = text_file.readlines()[offset:]
        raw_lines = [self._clean_example(ex) for ex in raw_lines]
        self.examples = [self._process_example_from_file(ex) for ex in raw_lines]
        self.i = 0
        text_file.close()
    
    def _clean_example(self, ex):
        """ Optionally pre-processes an input string before some tokenization.
            Only necessary for some datasets. """
        return ex
