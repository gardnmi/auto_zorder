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

  <h3 align="center">DLT Side Step</h3>

  <p align="center">
    Take the guesswork out of ZORDER
    <br />
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

![Alt Text](https://i.imgur.com/UUszUGT.png)

The project aims to remove the guesswork of selecting columns to be used in the ZORDER statement. It achieves this by analyzing the logged execution plan for each cluster provided and return the top n columns used to filter by users.

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

```python
from pyspark.sql.functions import *
from pyspark.sql.types import *
from dlt_sidestep import SideStep

pipeline_id =  spark.conf.get("pipelines.id", None)
g = globals()

if pipeline_id:
  import dlt

json_path = "/databricks-datasets/wikipedia-datasets/data-001/clickstream/raw-uncompressed-json/2015_2_clickstream.json"

step = """
@dlt.create_table(
  comment="The raw wikipedia click stream dataset, ingested from /databricks-datasets.",
  table_properties={
    "quality": "bronze"
  }
)
def clickstream_raw():
  return (
    spark.read.option("inferSchema", "true").json(json_path)
  )
"""
SideStep(step, pipeline_id, g)

if not pipeline_id:
  df = clickstream_raw()
  df.display()


step = """
@dlt.create_table(
  comment="Wikipedia clickstream dataset with cleaned-up datatypes / column names and quality expectations.",
  table_properties={
    "quality": "silver"
  }
)
@dlt.expect("valid_current_page", "current_page_id IS NOT NULL AND current_page_title IS NOT NULL")
@dlt.expect_or_fail("valid_count", "click_count > 0")
def clickstream_clean():
  return (
    dlt.read("clickstream_raw")
      .withColumn("current_page_id", expr("CAST(curr_id AS INT)"))
      .withColumn("click_count", expr("CAST(n AS INT)"))
      .withColumn("previous_page_id", expr("CAST(prev_id AS INT)"))
      .withColumnRenamed("curr_title", "current_page_title")
      .withColumnRenamed("prev_title", "previous_page_title")
      .select("current_page_id", "current_page_title", "click_count", "previous_page_id", "previous_page_title")
  )
"""
SideStep(step, pipeline_id, g)

if not pipeline_id:
  df = clickstream_clean()
  df.display()

```

![Alt Text](https://i.imgur.com/y1w6VBB.png)

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>
