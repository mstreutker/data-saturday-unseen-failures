file_path = "/workspaces/local-pyspark/data/warehouse_inventory_amsterdam.csv"
print(file_path.rsplit("_", maxsplit=1)[-1].replace(".csv", ""))
