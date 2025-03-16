import pandera as pa


class BaseDataFrame(pa.DataFrameModel):
    class Config:
        coerce = True
        strict = True
