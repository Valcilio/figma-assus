from pandas import DataFrame


from .datatransform import DataTransform
from .logger.logger_msg import LoggerMsg

class TimeSeriesModeling(DataTransform):

    def __init__(self, df: DataFrame, **kwargs):

        self.df = df.copy()
        self.logger = LoggerMsg('Time Series Modeling')

    