import os
import pandas as pd


def estandarizar_texto(serie: pd.Series, quitar_espacios: bool = True) -> pd.Series:
    texto = serie.str.lower().str.replace(r"[ .-]", "_", regex=True)
    return texto.str.strip() if quitar_espacios else texto


def procesar_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna().copy()

    data["monto_del_credito"] = (
        data["monto_del_credito"]
        .str.replace("$ ", "", regex=False)
        .str.replace(",", "")
        .astype(float)
    )

    columnas_a_categorizar = [
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for nombre_columna in columnas_a_categorizar:
        data[nombre_columna] = estandarizar_texto(
            data[nombre_columna], quitar_espacios=(nombre_columna != "barrio")
        ).astype("category")

    data["sexo"] = data["sexo"].str.lower().astype("category")
    data["estrato"] = data["estrato"].astype("category")
    data["comuna_ciudadano"] = data["comuna_ciudadano"].astype(int).astype("category")
    data["fecha_de_beneficio"] = pd.to_datetime(
        data["fecha_de_beneficio"], dayfirst=True, format="mixed"
    )

    data.drop_duplicates(inplace=True)
    return data


def pregunta_01():
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    df = procesar_dataframe(df)
    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";")
