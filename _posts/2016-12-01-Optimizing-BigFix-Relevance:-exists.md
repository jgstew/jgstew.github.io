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

- I am using `(folders "C:\Windows\Temp";folders "/tmp")` above because it is cross platform.
 - My preferred windows relevance of `folders "Temp" of windows folders` does not work cross platform.

### Similar Posts:

[The Way Bigfix Session Relevance Statements Are Written Matters (part1)](https://forum.bigfix.com/t/the-way-session-relevance-statements-webreports-are-written-matters/13663):
 - [BigFix Forum Post](https://forum.bigfix.com/t/the-way-session-relevance-statements-webreports-are-written-matters/13663) - make comments here
 - [GitHub Source File](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2015-06-18-The-way-BigFix-Session-Relevance-statements-are-written-matters-(part1).md) - suggest improvements here
 - [Website](http://jgstew.github.io/2015/06/18/The-way-BigFix-Session-Relevance-statements-are-written-matters-(part1).html) - generated GitHub Page

[The Way Bigfix Session Relevance Statements Are Written Matters (part2) Computer Names](https://forum.bigfix.com/t/the-way-session-relevance-statements-are-written-matters-part-2-computer-names/14340):
 - [BigFix Forum Post](https://forum.bigfix.com/t/the-way-session-relevance-statements-are-written-matters-part-2-computer-names/14340) - make comments here
 - [GitHub Source File](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2015-09-14-The-way-BigFix-Session-Relevance-statements-are-written-matters-(Part2)-Computer-Names.md) - suggest improvements here
 - [Website](http://jgstew.github.io/2015/09/14/The-way-BigFix-Session-Relevance-statements-are-written-matters-(Part2)-Computer-Names.html) - generated GitHub Page

[The Way Bigfix Session Relevance Statements Are Written Matters (part3) Whose](https://forum.bigfix.com/t/the-way-relevance-statements-are-written-matters-part3-whose/18785):
 - [BigFix Forum Post](https://forum.bigfix.com/t/the-way-relevance-statements-are-written-matters-part3-whose/18785) - make comments here
 - [GitHub Source File](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2016-10-11-The-way-BigFix-Session-Relevance-statements-are-written-matters-(Part3)-Whose.md) - suggest improvements here
 - [Website](http://jgstew.github.io/2016/10/11/The-way-BigFix-Session-Relevance-statements-are-written-matters-(Part3)-Whose.html) - generated GitHub Page

Optimizing Custom Filters:
 - https://forum.bigfix.com/t/optimizing-custom-filters/15022

### Related:

- https://developer.bigfix.com/relevance/reference/filesystem-object.html
- https://forum.bigfix.com/t/speeding-up-api-and-session-relevance-queries/15366/4
- https://forum.bigfix.com/t/relevance-to-retrieve-a-set-of-computer-objects-with-duplicate-names/14306/14
- https://forum.bigfix.com/t/solved-session-relevance-extracting-action-results-from-multiple-computers-in-an-efficient-way/18464
- https://forum.bigfix.com/t/sqlite-inspector-read-only-databases/13606/23
