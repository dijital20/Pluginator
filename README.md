# Pluginator
Just a simple script to generate random strings based on a template string and text files with fill-in choices.

## Usage
Pluginator.py TEMPLATE_STRING FILE1 [FILE2 FILE3 ...]

TEMPLATE_STRING should be a string containing one or more placeholders in curly braces {}. The placeholder names should correspond to the file names used for FILE1, FILE2, etc.

For instance:
Pluginator.py "This {food} is good." food.txt

This would print "This ____ is good." with the contents of the blank being replaced by a random line from food.txt.

## Optional parameters
--verbose will print verbose output.
-n will allow you to print n number of strings. So with the example above, adding -n 10 will print 10 random strings.
--help will display the usage.

Feel free to copy and reuse. This was just a simple proof of concept for a friend.
