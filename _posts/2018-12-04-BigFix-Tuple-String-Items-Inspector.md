

This will explore the use and usefulness of the BigFix Tuple String Items Inspector.

Consider this string with 4 elements within it:

    "0, one, 2, three"

With the Tuple String Items inspector, we can get any of them by their "index":

    Q: tuple string items 1 of "0, one, 2, three"
    A: one
    
Notice that the first item is at index 0 while the "second" is at 1

------------

Now consider this "Tuple" which contains strings, integers, and booleans:

    Q: (0,"one",2,"three", FALSE)
    A: 0, one, 2, three, False
    T: 0.078 ms
    I: singular ( integer, string, integer, string, boolean )
    
If it is cast as a string, we end up with a "Tuple String" much like in the first example above:

    Q: (it as string) of (0,"one",2,"three", FALSE)
    A: 0, one, 2, three, False
    T: 0.088 ms
    I: singular string
    
And now we could use the "Tuple String Items" inspector on it:

    Q: tuple string items 0 of (it as string) of (0,"one",2,"three", FALSE)
    A: 0
    T: 0.084 ms
    I: plural string
    
If "Tuple String Items" is used without specifying an "index" then it will just break up the Tuple String into a plural result, which can be a useful thing to do sometimes:

    Q: tuple string items of (it as string) of (0,"one",2,"three", FALSE)
    A: 0
    A: one
    A: 2
    A: three
    A: False
    T: 0.112 ms
    I: plural string
    

----------

### Other Examples:

    Q: ("zero";"one";"2";"three")
    A: zero
    A: one
    A: 2
    A: three
    T: 0.029 ms
    I: plural string

    Q: number of ("zero";"one";"2";"three")
    A: 4
    T: 0.039 ms
    I: singular integer

    Q: concatenations ", " of ("zero";"one";"2";"three, ?")
    A: zero, one, 2, three, ?
    T: 0.105 ms
    I: plural string

    Q: tuple string items 1 of concatenations ", " of  ("0";"one";"2";"three")
    A: one
    T: 0.110 ms
    I: plural string

    Q: tuple string items of concatenations ", " of  ("zero";"one";"2";"three, ?")
    A: zero
    A: one
    A: 2
    A: three
    A: ?
    T: 0.115 ms
    I: plural string

    Q: number of tuple string items of concatenations ", " of  ("zero";"one";"2";"three, ?")
    A: 5
    T: 0.160 ms
    I: singular integer
