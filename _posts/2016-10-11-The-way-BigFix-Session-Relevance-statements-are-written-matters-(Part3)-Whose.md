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

The reason that this works is because when statements are combined with `AND` inside of a `WHOSE` clause, the first statement to be false stops the evaluation and eliminates the result immediately. This means you want the fastest to evaluate items first in the `WHOSE` clause.
