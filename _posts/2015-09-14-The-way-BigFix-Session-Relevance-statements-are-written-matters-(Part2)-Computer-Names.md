I wrote a previous post about optimizing session relevance statements and why it matters. This is another example of the same.

----------

**The following info is based upon this:**  https://forum.bigfix.com/t/relevance-to-retrieve-a-set-of-computer-objects-with-duplicate-names/14306/11

@glbproject had a need to get the **set of computer objects that have duplicate names**, but in an environment with 250k clients this can be a challenge.

----------

There are many different session relevance statements below that all find the **set of computer objects with duplicate names**, but each one does so in a slightly different way. I'll explore why this is the case beneath each statement, but first, **some background:**

The complexity of the following relevance statements are related to how many computers are in the environment and how many of those computers have duplicate names. Increasing either the number of computers in the environment, or the number of computers with duplicate names will increase the complexity and the time to evaluate for the statements below.

All of the following relevance statements create an **[array](https://en.wikipedia.org/wiki/Array_data_structure)** of **[tuple](http://whatis.techtarget.com/definition/tuple)**s. You can't store the results of one relevance query and then use that in the context of a separate relevance query. If you want to accomplish something in pure relevance, then you have to do the work in a single query. **Tuple**s are the closest you can come in pure relevance to "**storing**" the results of a query and use it with a second query.

All of the tuples created in the following relevance statements involve the pairing of 2 different items. The first is the set of **all bes computers**. The second is the set of **duplicate computer names**. The pair of items in the tuple are then compared to remove all pairs that do not contain a computer with a name matching the duplicated name it is paired with.

All of the **arrays of tuples** created by the following relevance statements (except for the last one) have a size given by the **number of computers** *times* the **number of duplicate computer names**, which can be found with the following relevance statement:

    (number of bes computers) * (number of unique values whose (multiplicity of it > 1) of names of bes computers)

There is some inefficiency involved with the creation of the tuples themselves, so the more tuples, the slower the relevance. Also, the number of tuples also affects the amount of memory that the set of objects being operated on takes up. The more memory used, the less efficient the relevance evaluation. There are probably more factors involved in the efficiency of relevance, but it is hard to say what all of them are without some deeper diving into the code execution itself, which is not a simple thing to do.

----------

### Option #1 takes ~130 seconds in my environment:

    (name of it, id of it) of items 0 of it whose (name of item 0 of it = item 1 of it) of ( bes computers, unique values whose (multiplicity of it > 1) of names of bes computers )

This session relevance statement takes each computer object and pairs it with each of the duplicate computer names. This is taking the larger set and multiplying it by the smaller set. The time required to get each computer object is almost nothing, but the time required to get the set of duplicate names is much longer by comparison. It is the number of times that the set of duplicate names must be calculated is what needs to be optimized.

The number of times the set of duplicate names must be calculated in this case is **the number of computers**. This is a worst-case scenario.

### Option #2 takes ~0.490 seconds or more in my environment:

    (name of it, id of it) of items 1 of it whose (name of item 1 of it = item 0 of it) of ( unique values whose (multiplicity of it > 1) of names of bes computers, bes computers )

The only difference with this option and the above is the order or operations. This takes the set of duplicate names and pairs each one with each of the computer objects. This is taking the smaller set and multiplying it by the larger set. The resulting array of tuples is the same, but the time it takes to get it is not.

The number of times the set of duplicate names must be calculated in this case is just **once**, but the computer objects have to be grabbed and paired off with each duplicate name.

### Option #3 takes ~0.465 seconds or more in my environment:

    (name of it, id of it) of items 0 of it whose (name of item 0 of it = item 1 of it) of (bes computers, it) of (unique values whose (multiplicity of it > 1) of names of bes computers)

The only difference between this statement and the above is that the set of duplicate names is calculated first on its own, then it is paired off with the computer objects. This causes the set of duplicate names to be calculated outside of the tuple pairing process, which seems to make it more efficient.

### Option #4 takes ~0.450 seconds in my environment:

    (name of it, id of it) of items 0 of (bes computers, it) whose (name of item 0 of it = item 1 of it) of (unique values whose (multiplicity of it > 1) of names of bes computers)

In the case of all of the other relevance statements above, they create the array of tuples containing **the number of computers** times **the number of duplicate names** first, then filter that down to only contain the set of tuples where the name of the computer object matches the duplicate name it is paired with. This statement above seems to be more efficient due to filtering down the tuples as their being added to the array so that the resulting array only ever contains the final result. Doing the filtering as the array of tuples is being constructed slows down the building of the array, but it should also result in less total memory usage, which has the effect of speeding up the results.

### Option #5 takes ~0.420 seconds in my environment:

    (name of it, id of it) of items 1 of (it, bes computers) whose(name of item 1 of it = item 0 of it) of (unique values whose (multiplicity of it > 1) of names of bes computers)

The only difference between this statement and #4 is the order of the items in the tuple, but it seems to be more efficient.

### Option #6 takes ~0.022 seconds in my environment:

    (name of it, id of it) of items 1 of (it, bes computers) whose(name of item 1 of it is contained by item 0 of it) of ( set of unique values whose (multiplicity of it > 1) of names of bes computers )

This statement is different than all of the others. It places all of the duplicate computer names into a single **string set**. This single set is then paired off with all of the computer objects. This builds an array of tuples with a number of entries matching the **number of bes computers**. The trick is that the **whose** statement checks to see if the **name of the computer object** exists within the **string set**. This is slightly more complicated to evaluate than the whose statements in all of the other options above, but it is being done a significantly less number of times.

----------

**See my original post about optimizing Session Relevance here:**  https://forum.bigfix.com/t/the-way-session-relevance-statements-webreports-are-written-matters/13663

**Related:** https://forum.bigfix.com/t/optimizing-custom-filters/15022
