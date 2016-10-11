There are multiple ways to write the same relevance statement, which is both a blessing and a curse. In most cases I would recommend keeping relevance simple and optimized for human readability. I wouldn't recommend optimizing relevance unless there is a clear need, unless it makes it faster / simpler / and more readable all at the same time.

All that said, with relevance, and most especially Session Relevance, you need to be careful of how statements you write make use of recursion. This is often less of an issue in the case of typical relevance because the set of items being recursed is limited by the scope of a single client, but it can still be an issue.

----------

Here are some examples of Session Relevance that are equivalent but different in how they operate, and much different in terms of their speed of execution.

**More straightforward, but slower:** http://bigfix.me/relevance/details/3002412

```
names of fixlets whose(name of it does not contain "(Superseded)" AND name of it as lowercase contains "endpoint manager" AND name of it as lowercase contains "client" AND globally visible flag of it AND ( (it >= (it as version) of preceding text of first "." of (it as string) of maximum of (it as version) of agent versions of bes computers) of (it as version) of following text of last "-" of name of it ) ) of bes sites whose("BES Support" = name of it)
```

**More complicated, but faster:** http://bigfix.me/relevance/details/3002413

```
names of items 2 of (item 0 of it, (it as version) of following text of last "-" of name of item 1 of it, item 1 of it) whose(item 1 of it >= item 0 of it) of (it, fixlets whose(name of it does not contain "(Superseded)" AND name of it as lowercase contains "endpoint manager" AND name of it as lowercase contains "client" AND globally visible flag of it) of bes sites whose("BES Support" = name of it) ) of ( (it as version) of preceding text of first "." of (it as string) of maximum of (it as version) of agent versions of bes computers )
```

Both statements use recursion, but the first uses double recursion, while the second statement uses single recursion twice.

The first statement's speed is estimated by:  ( #Fixlets * time-per-fixlet ) * ( #computers * time-per-computer )

The second statement's speed is estimated by: ( #Fixlets * time-per-fixlet ) + ( #computers * time-per-computer )

Both statements may be relatively fast on a small deployment, but as the deployment grows in size, the time the first statement takes will grow significantly, while the second will not grow nearly as much.

This means that it is possible to write Session Relevance that will seem to work fine in the case of a small deployment, but will be slow in a medium sized deployment, and may become so slow in a large deployment that it will actually time out and never work successfully. This makes Session Relevance especially challenging to write, because a statement that is otherwise completely valid may never actually produce results only due to the execution time that would be required.


https://en.wikipedia.org/wiki/Recursion_(computer_science)

----------

**Related:**

- https://forum.bigfix.com/t/the-way-session-relevance-statements-are-written-matters-part-2/14340
- https://forum.bigfix.com/t/optimizing-custom-filters/15022
