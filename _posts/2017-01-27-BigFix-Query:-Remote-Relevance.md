---
published: false
---

# Work In Progress

BigFix query allows you to do dynamic remote relevance queries.

## SQL

Get all Query IDs with results:

    SELECT DISTINCT TOP (1000) 
          [QueryID]
      FROM [BFEnterprise].[dbo].[QUERYRESULTTEXT]

Get all Query IDs:

    SELECT TOP (1000) 
          [QueryID]
          ,[Operator]
          ,[CreationTime]
      FROM [BFEnterprise].[dbo].[QUERIES]


### Related:

- https://developer.bigfix.com/rest-api/api/bigfix_query.html
- https://forum.bigfix.com/t/ended-bay-area-bigfix-user-group-oct-13th-2016-in-emeryville-ca/18316/16
