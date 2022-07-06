<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Auto ZORDER</h3>

  <p align="center">
    Take the guesswork out of ZORDER
    <br />
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

![Alt Text](https://i.imgur.com/UUszUGT.png)

The project aims to remove the guesswork of selecting columns to be used in the ZORDER statement. It achieves this by analyzing the logged execution plan for each cluster provided and returns the top n columns that were used in filter/where clauses.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [python](https://www.python.org/)
- [spark](https://spark.apache.org/)
- [databricks](https://databricks.com/)
- [delta](https://delta.io/)

<p align="right">(<a href="#top">back to top</a>)</p>

### Prerequisites

Cluster log delivery

- You must setup a default destination for the cluster log delivery. For example, `dbfs:/cluster-log-delivery/0630-191345-leap375`. See the below link for more information on how to setup a cluster log deliver on databricks.
  - https://docs.databricks.com/clusters/configure.html#cluster-log-delivery

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation

pip install in your Databricks Notebook

```python
%pip install auto_zorder
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Example Usage

**Note**: If the cluster log delivery has not been active for very long then you may not see any results.

#### Basic Usage

```python
from auto_zorder import auto_zorder

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
from auto_zorder import auto_zorder

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
from auto_zorder import auto_zorder

optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1'],
                    optimize_table='my_db.my_table',
                    save_analysis='my_db.my_analysis'
                    )
```

#### Run auto zorder using analysis instead of cluster logs

```python
from auto_zorder import auto_zorder

optimize_cmd = auto_zorder(
                    use_analysis='my_db.my_analysis',
                    optimize_table='my_db.my_table'
                    )
```

#### Include additional columns and location in ZORDER

```python
from auto_zorder import auto_zorder

optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1', 'cluster_id_2'],
                    optimize_table='my_db.my_table',
                    use_add_cols=[('add_col1', 0), ('add_col2', 4)]
                    )

print(optimize_cmd)
>>> 'OPTIMIZE my_db.my_table ZORDER BY (add_col1, auto_col1, auto_col2, auto_col3, add_col2, auto_col4, auto_col5)'
```

#### Exclude columns in ZORDER

```python
from auto_zorder import auto_zorder

optimize_cmd = auto_zorder(
                    cluster_ids=['cluster_id_1', 'cluster_id_2'],
                    optimize_table='my_db.my_table',
                    exclude_cols=['col1']
                    )

print(optimize_cmd)
>>> 'OPTIMIZE my_db.my_table ZORDER BY (col2, col3, col4, col5, col6)'
```

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>
