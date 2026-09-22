import pandas as pd


def clean_column_names(df):
    df = df.copy()

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # Some datasets use "st", others use "state"
    if "st" in df.columns and "state" in df.columns:
        df["state"] = df["state"].fillna(df["st"])
        df = df.drop(columns=["st"])

    elif "st" in df.columns:
        df = df.rename(columns={"st": "state"})

    return df


def clean_invalid_values(df):
    df["gender"] = df["gender"].replace({
        "F": "F",
        "female": "F",
        "Femal": "F",
        "M": "M",
        "Male": "M"
    })

    df["state"] = df["state"].replace({
        "AZ": "Arizona",
        "Cali": "California",
        "WA": "Washington"
    })

    df["education"] = df["education"].replace({
        "Bachelors": "Bachelor"
    })

    df["customer_lifetime_value"] = (
        df["customer_lifetime_value"]
        .str.replace("%", "", regex=False)
    )

    df["vehicle_class"] = df["vehicle_class"].replace({
        "Sports Car": "Luxury",
        "Luxury SUV": "Luxury",
        "Luxury Car": "Luxury"
    })

    return df


def format_data_types(df):
    df["customer_lifetime_value"] = pd.to_numeric(
        df["customer_lifetime_value"],
        errors="coerce"
    )

    df["number_of_open_complaints"] = (
        df["number_of_open_complaints"]
        .str.split("/")
        .str[1]
    )

    df["number_of_open_complaints"] = pd.to_numeric(
        df["number_of_open_complaints"],
        errors="coerce"
    )

    return df


def handle_null_values(df):
    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(include="object").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    for column in categorical_columns:
        df[column] = df[column].fillna(df[column].mode()[0])

    for column in numeric_columns:
        df[column] = df[column].astype(int)

    return df


def remove_duplicates(df):
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    return df


def clean_data(df):
    df = clean_column_names(df)
    df = clean_invalid_values(df)
    df = format_data_types(df)
    df = handle_null_values(df)
    df = remove_duplicates(df)

    return df