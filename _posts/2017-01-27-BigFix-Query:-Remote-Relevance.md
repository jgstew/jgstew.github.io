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

Get (user, queryID, creationtime, mastheadusername) for all BFQueries

    SELECT TOP (1000) 
          [BFEnterprise].[dbo].[USERINFO].[Username]
    	  ,[BFEnterprise].[dbo].[QUERIES].[QueryID]
          ,[BFEnterprise].[dbo].[QUERIES].[CreationTime]
    	  ,[BFEnterprise].[dbo].[USERINFO].[MastheadUsername]
      FROM [BFEnterprise].[dbo].[QUERIES]
      INNER JOIN [BFEnterprise].[dbo].[USERINFO]
      ON [BFEnterprise].[dbo].[QUERIES].[Operator]=[BFEnterprise].[dbo].[USERINFO].[MastheadUsername];


### Related:

- https://developer.bigfix.com/rest-api/api/bigfix_query.html
- https://forum.bigfix.com/t/ended-bay-area-bigfix-user-group-oct-13th-2016-in-emeryville-ca/18316/16
