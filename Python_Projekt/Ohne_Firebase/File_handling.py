import sys

def load(file):
    try:
        with open(file) as in_file:
            loaded_txt = in_file.read().lower().strip("").split('\n')
                
            return loaded_txt
        
    except IOError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file),
              file=sys.stderr)
        sys.exit(1)