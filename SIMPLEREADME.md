### Installation

pip install in your Databricks Notebook

```python
%pip install auto_zorder
```

### Example Usage

**Note**: If the cluster log delivery has not been active for very long then you may not see any results.

#### Basic Usage

```python
optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1', 'cluster_id_2'],
                    optimize_table='my_db.my_table'
                    )

print(optimize_cmd)
>>> 'OPTIMIZE my_db.my_table ZORDER BY (col1, col2, col3, col4, col5)'

# To run the OPTIMIZE Command
spark.sql(optimize_cmd)
```

#### Limit the Number of ZORDER columns

```python
optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1', 'cluster_id_2'],
                    optimize_table='my_db.my_table',
                    number_of_cols=2
                    )

print(optimize_cmd)
>>> 'OPTIMIZE my_db.my_table ZORDER BY (col1, col2)'
```

#### Save auto zorder analysis

```python
optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1'],
                    optimize_table='my_db.my_table',
                    save_analysis='my_db.my_analysis'
                    )
```

#### Run auto zorder using analysis instead of cluster logs

```python
optimize_cmd = auto_zorder(
                    use_analysis='my_db.my_analysis',
                    optimize_table='my_db.my_table'
                    )
```

#### Include additional columns and location in ZORDER

```python
optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1', 'cluster_id_2'],
                    optimize_table='my_db.my_table',
                    use_add_cols=[('add_col1', 0), ('add_col2', 4)]
                    )

print(optimize_cmd)
>>> 'OPTIMIZE my_db.my_table ZORDER BY (add_col1, auto_col1, auto_col2, auto_col3, add_col2, auto_col4, auto_col5)'
```
