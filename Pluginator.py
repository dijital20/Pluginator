import os.path

from random import choice
from re import findall
from sys import argv


class Pluginator(object):
    """
    Take a template string, and one or more text files with values for the
    placeholders, and replace the placeholders with a random value from the
    file.
    """
    ptrn_placeholder = r'\{([\w\d\- ]+)\}'

    def __init__(self, verbose=False):
        """
        Prepares a Pluginator object for use.
        """
        self.verbose = bool(verbose) if verbose else False
        self.values = dict()

    def add_file(self, file_path):
        """
        Add a file of choices to the dictionary of choices.

        Args:
            file_path (str): Path of the file to read. This should be a plain
                text file.

        Returns:
            True if successful, False if not.
        """
        if not os.path.isfile(file_path):
            print('ERROR: File {0} is not found.'.format(file_path))
            return False
        fname = '.'.join(os.path.basename(file_path).split('.')[:-1])
        try:
            with open(file_path, mode='r') as f:
                self.values[fname] = [l.strip() for l in f.readlines()]
        except (IOError, OSError) as e:
            print('ERROR: {0}'.format(e))
            return False
        if self.verbose:
            print('Added {0} as {1} with {2} choices.'.format(
                file_path, fname, len(self.values[fname])))
        return True

    def build_template(self, template):
        """
        Build a string based on the template string and our dictionary of
        values.

        Args:
            template (str): String with placeholders to replace.

        Returns (str, None):
            A string with random choices replacing the placeholders, or None if
            one or more of the placeholders are missing.
        """
        placeholders = list(set(findall(self.ptrn_placeholder, tmplt_str)))
        if not all([p in self.values for p in placeholders]):
            print('ERROR: One or more placeholders missing values.')
            return None
        vals = dict()
        for k in self.values:
            vals[k] = choice(self.values[k])
        return template.format(**vals)


if __name__ == '__main__':
    # Get the args and pull the script name.
    args = argv
    script_name = args.pop(0)

    # Build the usage string.
    usage = '{0} template_string file1.txt file2.txt...\n' \
            '\n' \
            'Where:\n' \
            'template_string    A string with placeholders which will be \n' \
            '                   replaced. Placeholders should be enclosed \n' \
            '                   in curly braces and contain the filename \n' \
            '                   without extension in which the choices \n' \
            '                   reside. \n' \
            'file1.txt          One or more text files containing choices \n' \
            '                   for a given placeholder. \n'.format(
        os.path.basename(script_name))

    # Handle help param
    if '--help' in args:
        print(usage)
        exit(0)

    # Handle verbose param
    verbose = False
    if '--verbose' in args:
        verbose = True
        args.remove('--verbose')

    # Handle -n param
    num = 1
    if '-n' in args:
        pos = args.index('-n')
        try:
            num = int(args.pop(pos+1))
        except ValueError as e:
            print('ERROR: {0}'.format(e))
        args.pop(pos)
    if verbose:
        print('Number of strings to generate set to {0}'.format(num))

    # Check that we have enough args
    if len(args) < 2:
        print('ERROR: Not enough arguments were specified')
        print(usage)
        exit(1)

    # Create the object, and do the damn thing.
    p = Pluginator(verbose=verbose)
    tmplt_str = args.pop(0)
    files = args
    for f in files:
        if not p.add_file(f):
            print(usage)
            exit(2)
    print('\n{0}'.format(
        '\n'.join([p.build_template(tmplt_str) for l in range(num)])
    ))
