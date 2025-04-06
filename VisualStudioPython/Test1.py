import re
import pandas as pd

def extract_tables_and_schemas(sql_script):
    """
    Extracts table names and schema names from a SQL script.

    Args:
        sql_script (str): The SQL script as a string.

    Returns:
        list: A list of dictionaries with keys 'Table Name', 'Schema Name', and 'File Name'.
    """
    # Regex pattern to match schema.table or standalone table names
    schema_table_pattern = re.compile(
        r"(?:FROM|JOIN|INTO|UPDATE|TABLE)\s+"
        r"(?:\[([a-zA-Z_][a-zA-Z0-9_]*)\]\.|([a-zA-Z_][a-zA-Z0-9_]*)\.)?"  # Match schema (optional)
        r"(?:\[([a-zA-Z_][a-zA-Z0-9_]*)\]|([a-zA-Z_][a-zA-Z0-9_]*))",  # Match table
        re.IGNORECASE
    )

    results = []
    seen = set()  # To avoid duplicates

    # Match schema.table or standalone table names
    for match in schema_table_pattern.findall(sql_script):
        schema = match[0] or match[1]  # Schema part
        table = match[2] or match[3]  # Table part

        if table and (schema, table) not in seen:
            results.append({
                "Table Name": table,
                "Schema Name": schema if schema else "",  # Add schema if present
                "File Name": "N/A"  # Placeholder for file name
            })
            seen.add((schema, table))

    return results

# Example usage
if __name__ == "__main__":
    # sql_script = """
    # SELECT * FROM [sales].[orders] o
    # JOIN public.[customers] c ON o.customer_id = c.customer_id
    # WHERE EXISTS (
    #     SELECT 1 FROM [temp].transactions t WHERE t.order_id = o.order_id
    # );
    # INSERT INTO hr.[employees] (id, name) VALUES (1, 'John Doe');
    # UPDATE [finance].[payroll] SET salary = salary * 1.1 WHERE department_id = 5;
    # """


    sql_script = """
    CREATE VIEW [rpt].[CDR ORDER_Pre0]
AS
WITH [StartEndDate]
AS (
   SELECT

       --'20200101' AS [StartDate],
       --'20201231' AS [EndDate]

	     FORMAT( DATEADD(dd, 1,  EOMONTH(DATEADD(MONTH, -4, GETDATE())) ), 'yyyyMMdd') [StartDate], -- Added on 6 Jan 2021
		FORMAT( EOMONTH(DATEADD(MONTH, 9, GETDATE())) , 'yyyyMMdd')  [EndDate]
	   
	   
	   )
,[Document]
AS (SELECT *
    FROM
    (
        SELECT [Item Data].[VBELN: (PK) Sales Document] AS [Sales Order],
               [Item Data].[POSNR: (PK) Sales Document Item] AS [item Number],
              

               CASE
                   WHEN [Item Data].[PSTYV: Sales Document Item Category] IN ( 'ZTPS', 'ZTXV', 'ZSE', 'ZBLK', 'ZLAB',
                                                                               'ZTAG', 'ZTAN', 'ZBLE', 'ZTAL', 'ZTCS',
                                                                               'ZTCT', 'ZREN', 'ZRNN', 'ZTAX', 'ZTPR',
                                                                               'Z1XS', 'ZBTL', 'ZFBK', 'ZFTN', 'ZQ01',
                                                                               'ZRET'
                                                                             ) THEN
                       COALESCE(
                                   [Document].[LDDAT_SIMP_DT: (GC) Loading Date],
                                   [Document].[ZZFIRST_DATE_SIMP_DT: (GC) Date]
                               )
                   --WHEN [Item Data].[PSTYV: Sales document item category] = 'ZTAN' THEN COALESCE([Document].[LDDAT_SIMP_DT: (GC) Loading Date], [Document].[ZZFIRST_DATE_SIMP_DT: (GC) Date])
                   WHEN [Item Data].[PSTYV: Sales Document Item Category] = 'AGN' THEN
                       [Document].[WADAT_SIMP_DT: (GC) Goods Issue Date]
                   ELSE
                       [Document].[EDATU_SIMP_DT: (GC) Schedule line date]
               END AS [Expected Ship Date],
               ROW_NUMBER() OVER (PARTITION BY [Item Data].[VBELN: (PK) Sales Document],
                                               [Item Data].[POSNR: (PK) Sales Document Item]
                                  ORDER BY [Document].[ETENR: (PK) Schedule Line Number] DESC
                                 ) AS RN,
               [Item Data].[PSTYV: Sales Document Item Category] AS QDOC_Type,
               [Item Data].[WERKS: Plant (Own or External)] AS [Plant Key],
               [Item Data].[ZZBASE_CODE: Base Code] AS [Base Code Key],
               [Item Data].[MATNR: Material Number],
               [Item Data].[MANDT: (PK) Client] [Client],
               [Document].[LDDAT: Loading Date],
               [Document].[MBDAT: Material Staging/Availability Date],
               [Document].[WADAT: Goods Issue Date],
               [Document].[EDATU: Schedule line date], 
			   [Document].[EDATU_SIMP_DT: (GC) Schedule line date], --25 March changes 
			   [Document].[ZZNEGDTCHNG: Date Change Initiated By] --Added by Lakshmi Harika on 24-02-2021
        FROM LIB_EDW_RTP.bv.[VBEP: Sales Document: Schedule Line Data] [Document] WITH (NOLOCK)
            LEFT JOIN LIB_EDW_RTP.bv.[VBAP: Sales Document: Item Data] [Item Data] WITH (NOLOCK)
                ON [Document].[VBELN: (PK) Sales Document] = [Item Data].[VBELN: (PK) Sales Document]
                   AND [Item Data].[POSNR: (PK) Sales Document Item] = Document.[POSNR: (PK) Sales Document Item]
				   AND [Item Data].[MANDT: (PK) Client] = '020'
        WHERE [Document].[MANDT: (PK) Client] = '020'
    --and [Document].[VBELN: (PK) Sales Document]   IN ( '0008114187' ,'0007866982') --IN  ( '0008125273', '0008079074','0008027992')
    ) A
    WHERE [RN] = 1
          AND [Expected Ship Date]
          BETWEEN
          (
              SELECT [StartDate] FROM StartEndDate
          ) AND
          (
              SELECT [EndDate] FROM StartEndDate
          )
	)
SELECT *
FROM [Document];
GO
"""
    results = extract_tables_and_schemas(sql_script)

    # Export results to Excel
    df = pd.DataFrame(results)
    df.to_excel("tables_and_schemas.xlsx", index=False)

    print("Results exported to tables_and_schemas.xlsx")
