%load_ext autoreload
%autoreload 2

import logging
from utility_functions.db import Db
logging.basicConfig( level=logging.DEBUG)


model=Db()
#model.drop_stocks_table()
model.create_stock_table()
#model.delete_data(symbol)


#upsert_data(symbol,data)

#model.get_data_stat(symbol)