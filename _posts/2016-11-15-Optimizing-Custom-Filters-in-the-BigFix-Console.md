First, let me say, that I know very little about how Custom Filters work under the hood. I'm assuming it uses Session Relevance or perhaps a SQL query. In either case, the following should apply.

The order of the filter criteria you set matters for Custom Filters. In general you want the most amount of items to be filtered out by the first statement so that any subsequent filters have less items to work with. It also matters which filter criteria are "easier" to evaluate than others. These same concepts apply to optimizing Relevance & Session Relevance.

----------

**This example is not optimal:**

![Unoptimized Console Filter](http://jgstew.github.io/images/BFilterOptimizing/ConsoleFilter.PNG)

One of the most significant issues is that the filter `Visibility equals Visible` filters out 0 items most of the time. This criteria should go last, and not second.

----------

**This example is more optimal:**

![Optimized Console Filter](http://jgstew.github.io/images/BFilterOptimizing/OptimizedConsoleFilter.PNG)

Typically in session relevance it is best to filter down to a specific site before filtering based upon the names of all fixlets in all sites. The reason is there is a much smaller set of sites in total to compare and getting just a specific site will filter out the most items with the least effort.

The next is a bit of a toss up. In this case I am getting only the items that contain `Firefox` and then filtering out the items that contain `(Superseded)`. It may actually be the case that filtering out the `(Superseded)` items first would actually reduce the set of items quite a lot in this particular case, but I still feel that this order makes more sense logically.

There can be a tension between optimizing the order of filtering to be the most optimal in terms of performance, without sacrificing the understandability of it. In general, I am against making significant sacrifices in logical flow and understandability only to achieve a small performance gain.

----------

**Related:**

- https://forum.bigfix.com/t/the-way-session-relevance-statements-webreports-are-written-matters/13663
- https://forum.bigfix.com/t/the-way-session-relevance-statements-are-written-matters-part-2/14340
- https://forum.bigfix.com/t/is-it-possible-to-get-the-underlying-session-relevance-that-powers-a-custom-filter/15008
