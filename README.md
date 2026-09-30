# inventory-report-py

Scripts we use at the shop to check stock, work out reorders and print the weekly report.

```
python report.py data/stock.csv data/sales.csv
```

Purchase orders for low stock, one file per supplier:

```
python orders.py data/stock.csv data/sales.csv          # write orders/ files
python orders.py data/stock.csv data/sales.csv --send   # and email them
```
