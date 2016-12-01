The way BigFix relevance is written matters. There are usually many ways to get the same result with relevance, but generally the faster the relevance can execute, the better. The more often a relevance statement is used or evaluated, the more speed matters.

One particularly important example is using `exists`. Using `exists` actually prevents the relevance statement that follows it from fully evaluating all possible items, because as soon as there is at least 1 result, then `exists` is satisfied and no further evaluation is required.

### Example:

The following 2 statements are equivalent. They will always return the same result in all cases.

#### Slower:

    Q: 0 < number of descendants of (folders "C:\Windows\Temp";folders "/tmp")
    A: True
    T: 11.246 ms
    I: singular boolean

#### Faster:

    Q: exists descendants of (folders "C:\Windows\Temp";folders "/tmp")
    A: True
    T: 0.354 ms
    I: singular boolean
    
The first example, which does not use `exists`, actually needs to count up every single file within the folder before comparing it to 0. This means the statement will be slower the more files there are in the folder in question.

The second example, which does use `exists`, does not actually get every file within the folder. Instead, as soon as `descendants` returns a single result, `exists` is satisfied and evaluation stops.

The strange part of this example is the fact that both use `descendants` which is an inspector that would typically return all of the file objects within the given folder. Putting `exists` in front of `descendants` like this actually changes the behavior of the `descendants` inspector, somehow letting it know that it only cares if there is at least one result and not all results.

----------

### Notes:

### Related:

- https://developer.bigfix.com/relevance/reference/filesystem-object.html
