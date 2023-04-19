from src.shared.storage import Database, DataFrameStorage


def get_classification_df():
    classification_df = DataFrameStorage("classification", db=Database.SHARED).get(
        "combined"
    )
    classification_df = classification_df.set_index("id")
    return classification_df
