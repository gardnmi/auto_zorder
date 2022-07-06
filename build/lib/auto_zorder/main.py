from pyspark.sql import functions as f
from pyspark.sql.types import *
import re
from typing import List, Tuple


def auto_zorder(
    optimize_table: str,
    number_of_cols: int = 5,
    cluster_ids: List[str] = None,
    save_analysis: str = None,
    use_analysis: str = None,
    use_add_cols: List[Tuple[str, int]] = None,
    display_analysis: bool = False,
) -> str:

    """
    ZORDER by the top n most filtered columns

    This function parses the spark event logs to determine the
    top n most filtered columns in a table.  The event logs must be
    setup using the dbfs with default configurations in databricks.

    See: https://docs.databricks.com/clusters/configure.html#cluster-log-delivery-1

    Parameters
    ----------
    optimize_table : str
        The table you want to OPTIMIZE.
    number_of_cols : int, default 5
        The number of columns you want to include in you ZORDER excluding `use_add_cols`.
    cluster_ids : List[str], default None
        The event logs to be scanned.  The root log folder name must match the cluster id. 
    save_analysis : str, default None
        Location to save the analysis results.  Saved results can be used in place of `cluster_ids`.
    use_analysis : str, default None
        If analysis results have been saved. The table can be used instead of scanning the event logs.
    use_add_cols : List[Tuple[str, int]], default None
        Add additional columns not included in the auto zorder
    display_analysis : bool, default False
        Display the analyzed results

    Returns
    -------
    str
        An OPTIMIZE statement with ZORDER by the top n filters.

    See Also
    --------
    https://docs.databricks.com/delta/optimizations/file-mgmt.html#z-ordering-multi-dimensional-clustering

    Examples
    --------
    >>> auto_zorder(
        cluster_ids=['cluster_id_1', 'cluster_id_2'], 
        optimize_table='my_db.my_table'
        )
    'OPTIMIZE my_db.my_table ZORDER BY (col1, col2, col3, col4, col5)'
    >>> auto_zorder(
        cluster_ids=['cluster_id_1', 'cluster_id_2'], 
        optimize_table='my_db.my_table',
        number_of_cols=4,
        use_add_cols=[('add_col1', 0)]
        )
    'OPTIMIZE my_db.my_table ZORDER BY (add_col1, col1, col2, col3, col4)'
    >>> auto_zorder(
        use_analysis='my_db.my_zorder_analysis', 
        optimize_table='my_db.my_table',
        number_of_cols=3,
        )
    'OPTIMIZE my_db.my_table ZORDER BY (col1, col2, col3)'
    """

    def extract_all_fields(col: f.Column) -> f.Column:
        # can't figure out how to get the spark extract_all to extract what I need
        # using python instead

        matches = re.findall("\([^(]*?\)", col)
        clean_matches = list(
            set(
                [
                    match.replace("(", "").replace(")", "").split(",")[0]
                    for match in matches
                ]
            )
        )

        return clean_matches

    extract_all_fields_udf = f.udf(extract_all_fields, ArrayType(StringType()))

    if use_analysis:
        df = spark.table(use_analysis)
    else:
        event_log_paths = [f"/cluster-logs/{id}/eventlog" for id in cluster_ids]
        df = spark.read.json(event_log_paths, recursiveFileLookup=True)

    df = (
        df.filter(f.col("physicalPlanDescription").like("%(_) Scan parquet%"))
        .withColumn("file_name", f.input_file_name())
        .select(["physicalPlanDescription", "time", "file_name"])
    )

    #   df.display()

    df = (
        df.withColumn("operator", f.split("physicalPlanDescription", "\n\n"))
        .withColumn("operator", f.explode("operator"))
        .filter(
            (f.col("operator").like("%(_) Scan parquet%"))
            & (f.col("operator").contains("PushedFilters:"))
        )
        .withColumn("stages", f.split("operator", "\n"))
        .withColumn("filter_table", f.explode("stages"))
        .filter(f.col("filter_table").contains(") Scan parquet "))
        .withColumn("filter_table", f.element_at(f.split("filter_table", " "), -1))
        .filter(f.col("filter_table") != "")
        .withColumn("filter_columns", f.explode("stages"))
        .filter(f.col("filter_columns").contains("PushedFilters:"))
        .withColumn("filter_columns", extract_all_fields_udf("filter_columns"))
    )

    if display_analysis:
        df.display()

    if save_analysis:
        (
            df.write.mode("overwrite")
            .option("overwriteSchema", "true")
            .saveAsTable(f"{save_analysis}")
        )

        spark.sql(f"OPTIMIZE {save_analysis} ZORDER BY (filter_table)")

    df = (
        df.withColumn("filter_columns", f.explode("filter_columns"))
        .filter(f.col("filter_table") == optimize_table)
        .groupby("filter_columns")
        .count()
        .orderBy("count", ascending=False)
        .limit(number_of_cols)
    )

    df = df.collect()

    zorder_cols = [col.filter_columns for col in df]

    if use_add_cols:
        for col in use_add_cols:

            # Remove if column included in auto zorder
            if col[0] in zorder_cols:
                i = zorder_cols.index(col[0])
                zorder_cols.pop(i)

            # Insert column into list of auto zorder
            zorder_cols.insert(col[1], col[0])

    if display_analysis:
        display(df)

    optimize_command = (
        f"""OPTIMIZE {optimize_table} ZORDER BY ({', '.join(zorder_cols)})"""
    )

    return optimize_command

