

Consider this string with 4 elements within it:

    "0, one, 2, three"

With the Tuple String Items inspector, we can get any of them by their "index":

    Q: tuple string items 1 of "0, one, 2, three"
    A: one
    
Notice that the first item is at index 0 while the "second" is at 1

------------

Now consider this "Tuple" which contains strings, integers, and booleans:

    (0,"one",2,"three", FALSE)
    
If it is cast as a string, we end up with a "Tuple String" much like in the first example above:

    Q: (it as string) of (0,"one",2,"three", FALSE)
    A: 0, one, 2, three, False
    
And now we could use the "Tuple String Items" inspector on it:

    Q: tuple string items 0 of (it as string) of (0,"one",2,"three", FALSE)
    A: 0
    
