import datetime

import great_expectations as gx
import pandas as pd
from great_expectations.render.renderer import *

print(gx.__version__)

# Create Data Context.
context = gx.get_context()

# Initialize the data docs site
base_directory = r"/workspaces/data-saturday-unseen-failures/demo/docs"
site_config = {
    "class_name": "SiteBuilder",
    "site_index_builder": {"class_name": "DefaultSiteIndexBuilder"},
    "store_backend": {
        "class_name": "TupleFilesystemStoreBackend",
        "base_directory": base_directory,
    },
}
site_name = "my_data_docs_site"
context.add_data_docs_site(site_name=site_name, site_config=site_config)

# Connect to data.
# Create Data Source, Data Asset, Batch Definition, and Batch.
data_source = context.data_sources.add_pandas("pandas")
data_asset = data_source.add_dataframe_asset(name="inventory")
batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")

# Create a new expectation suite
suite = context.suites.add(
    gx.core.expectation_suite.ExpectationSuite(name="great-expectations-demo")
)

# Create Validation Definition.
validation_definition = context.validation_definitions.add(
    gx.core.validation_definition.ValidationDefinition(
        name="validation definition",
        data=batch_definition,
        suite=suite,
    )
)
validations = []
validations.append(validation_definition)

# Create an expectation to validate if the Current Stock Quantity falls within an expected range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="Current Stock Quantity", min_value=0, max_value=125000
    )
)

# Create an expectation to validate if the mean of Current Stock Quantity falls within an expected range
suite.add_expectation(
    gx.expectations.ExpectColumnMeanToBeBetween(
        column="Current Stock Quantity", min_value=5000, max_value=6000
    )
)

# Create an expectation to validate if the Date contains recent data
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        column="Date", min_value=datetime.datetime(2024, 9, 7)
    )
)

# Create an expectation to validate if the Unit is always L
suite.add_expectation(
    gx.expectations.ExpectColumnDistinctValuesToEqualSet(column="Units", value_set=["L"])
)

# Create an action to update the Data Docs once a validation has run
actions = [
    gx.checkpoint.actions.UpdateDataDocsAction(name="update_my_site", site_names=[site_name])
]

# Create Checkpoint, run Checkpoint, and capture result.
checkpoint = context.checkpoints.add(
    gx.checkpoint.checkpoint.Checkpoint(
        name="checkpoint",
        validation_definitions=validations,
        actions=actions,
    )
)

# Run the validations for every inventory-file.
DATA_FOLDER = r"/workspaces/data-saturday-unseen-failures/data"
files = [
    "warehouse_inventory_amsterdam.csv",
    "warehouse_inventory_breda.csv",
    "warehouse_inventory_culemborg.csv",
    "warehouse_inventory_delft.csv",
    "warehouse_inventory_emmen.csv",
    "warehouse_inventory_farmsum.csv",
]

for file in files:
    df = pd.read_csv(rf"{DATA_FOLDER}/{file}", sep=";", thousands=",")

    # Set proper datatypes
    df["Current Stock Quantity"] = df["Current Stock Quantity"].apply(pd.to_numeric)
    df["Date"] = df["Date"].apply(pd.to_datetime)

    runidentifier = gx.checkpoint.checkpoint.RunIdentifier(f"test-{file}")
    checkpoint_result = checkpoint.run(batch_parameters={"dataframe": df}, run_id=runidentifier)

context.build_data_docs()
# context.open_data_docs()
