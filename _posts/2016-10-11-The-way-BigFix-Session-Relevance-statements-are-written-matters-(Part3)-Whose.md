The order of operations within a complex WHOSE clause matters in BigFix Relevance but especially in Session Relevance.

A WHOSE clause takes plural results (similar to arrays) and filters out the unwanted items.

Here are 2 examples:

    Q: number of it whose(it contains "b") of ("b";"abc";"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab";"aaaaaaaaaaaaaaaaac")
    A: 3
    T: 0.054 ms
    I: singular integer

    Q: number of it whose(it starts with "a") of ("b";"abc";"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab";"aaaaaaaaaaaaaaaaac")
    A: 3
    T: 0.043 ms
    I: singular integer
    
Generally, `starts with` will be faster than `contains` because `contains` is more dependant upon the length of the string being examined than `starts with` is.

This means that if you want to know which strings start with `a` and contain `b`, you should first filter by `starts with` before using `contains`. Both of the following examples are equivalent, but the first is faster:

    Q: number of it whose(it starts with "a" AND it contains "b") of ("b";"abc";"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab";"aaaaaaaaaaaaaaaaac")
    A: 2
    T: 0.037 ms
    I: singular integer

    Q: number of it whose(it contains "b" AND it starts with "a") of ("b";"abc";"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab";"aaaaaaaaaaaaaaaaac")
    A: 2
    T: 0.049 ms
    I: singular integer

The reason that this works is because when statements are combined with `AND` inside of a `WHOSE` clause, the first statement to be false stops the evaluation and eliminates the result immediately.

This means you generally want the fastest to evaluate items first in the `WHOSE` clause, except in rare cases in which you also have to care about how many of the results the statement eliminates. If a statement is very fast, but only eliminates a small percentage of the results, then it may be better to use a statement that is a tad slower but eliminates a larger set of the results so that the subsequent clauses have less items to evalute. 

-----

Now lets take a real world example using Session Relevance and try to optimize it. 

The use case is to dynamically query for a running Firefox patch baseline.

This version takes ~40ms:

    number of bes actions whose(name of it as lowercase contains "Firefox" as lowercase AND source of source fixlet of it contains "RESTAPI: Generate " AND baseline flag of source fixlet of it AND "jgstew" = name of issuer of it AND name of it as lowercase contains "Windows" as lowercase AND "Open" = state of it)

Lets see if moving the check for state to the front: (~20ms)

    number of bes actions whose("Open" = state of it AND name of it as lowercase contains "Firefox" as lowercase AND source of source fixlet of it contains "RESTAPI: Generate " AND baseline flag of source fixlet of it AND "jgstew" = name of issuer of it AND name of it as lowercase contains "Windows" as lowercase)

This turns out to be twice as fast! But why? Let's break it down individually and see.

