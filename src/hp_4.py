# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    old_dates_innew = [datetime.strptime(date_old, "%Y-%m-%d").strftime('%d %b %Y') for date_old in old_dates]
    return old_dates_innew

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    listres = []
    
    strd = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        listres.append(strd + timedelta(days=i))
        
    return listres


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    
    res1 = date_range(start_date, len(values))
    i = list(zip(res1, values))
    return i

def fees_report(infile, outfile):
    
    infileheaders = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".split(','))
    feesData = defaultdict(float)
    
    with open(infile, 'r') as f:
        lines = DictReader(f, fieldnames=infileheaders)
        rows = [row for row in lines]

    rows.pop(0)
       
    for each_line in rows:
       
        patronID = each_line['patron_id']
        date_due = datetime.strptime(each_line['date_due'], "%m/%d/%Y")
        date_returned = datetime.strptime(each_line['date_returned'], "%m/%d/%Y")
        dl = (date_returned - date_due).days
        feesData[patronID]+= 0.25 * dl if dl > 0 else 0.0
        
    feeset = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in feesData.items()
    ]
    with open(outfile, 'w') as f:
        
        writer = DictWriter(f,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(feeset)



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
