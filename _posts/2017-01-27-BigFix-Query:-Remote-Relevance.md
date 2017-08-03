# BigFix Query Info

BigFix query allows you to do dynamic remote relevance queries.

For some reason, there is no session relevane or rest api to get the list of BFQueries that already exist. This means that the only way to get this info is with SQL.

## SQL

- https://www.codeproject.com/articles/33052/visual-representation-of-sql-joins

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

Get (username, queryID, creationtime, mastheadusername) for all BFQueries

    SELECT TOP (1000) 
          [BFEnterprise].[dbo].[USERINFO].[Username]
    	  ,[BFEnterprise].[dbo].[QUERIES].[QueryID]
          ,[BFEnterprise].[dbo].[QUERIES].[CreationTime]
    	  ,[BFEnterprise].[dbo].[USERINFO].[MastheadUsername]
      FROM [BFEnterprise].[dbo].[QUERIES]
      INNER JOIN [BFEnterprise].[dbo].[USERINFO]
      ON [BFEnterprise].[dbo].[QUERIES].[Operator]=[BFEnterprise].[dbo].[USERINFO].[MastheadUsername];

Get (QueryID, Operator, Creationtime) for all BFQueries with results:

    SELECT DISTINCT TOP (1000) 
          [BFEnterprise].[dbo].[QUERYRESULTTEXT].[QueryID]
    	  ,[BFEnterprise].[dbo].[QUERIES].[Operator]
    	  ,[BFEnterprise].[dbo].[QUERIES].[CreationTime]
      FROM [BFEnterprise].[dbo].[QUERYRESULTTEXT]
      INNER JOIN [BFEnterprise].[dbo].[QUERIES]
      ON [BFEnterprise].[dbo].[QUERIES].[QueryID]=[BFEnterprise].[dbo].[QUERYRESULTTEXT].[QueryID]

Get (username, queryID, CreationTime, mastheadusername) for all BFQueries with results:

    SELECT DISTINCT TOP (1000) 
          [BFEnterprise].[dbo].[USERINFO].[Username]
    	  ,[BFEnterprise].[dbo].[QUERYRESULTTEXT].[QueryID]
    	  ,[BFEnterprise].[dbo].[QUERIES].[CreationTime]
    	  ,[BFEnterprise].[dbo].[USERINFO].[MastheadUsername]
      FROM [BFEnterprise].[dbo].[QUERYRESULTTEXT]
      INNER JOIN [BFEnterprise].[dbo].[QUERIES]
    	ON [BFEnterprise].[dbo].[QUERIES].[QueryID]=[BFEnterprise].[dbo].[QUERYRESULTTEXT].[QueryID]
      INNER JOIN [BFEnterprise].[dbo].[USERINFO]
      ON [BFEnterprise].[dbo].[QUERIES].[Operator]=[BFEnterprise].[dbo].[USERINFO].[MastheadUsername];
      

### Related:

- https://developer.bigfix.com/rest-api/api/bigfix_query.html
- https://forum.bigfix.com/t/ended-bay-area-bigfix-user-group-oct-13th-2016-in-emeryville-ca/18316/16
