import sys

def load(file):
    Produkte = {}
    """Open a text file & turn contents into a list of lowercase strings."""
    try:
        with open(file) as in_file:
            loaded_txt = in_file.read().lower().strip("").split('\n')
            for line in loaded_txt:
                line = str(line).split(',')
                Produkte[str(line[0])] = (line[1], line[2::])
                
            return Produkte
        
    except IOError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file),
              file=sys.stderr)
        sys.exit(1)