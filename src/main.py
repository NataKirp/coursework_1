from src.reports import spending_by_category
from src.services import df_to_dict, cashback_analysis
from src.utils import read_excel_file
from src.views import main_page

if __name__ == '__main__':
    date_input = '2020-05-20 12:00:00'
    result_views = main_page(date_input)
    print(result_views)

    df = read_excel_file('../data/operations.xlsx')
    df = df.fillna(0)
    data = df_to_dict(df)

    result_services = cashback_analysis(data, 2018, 3)
    print(result_services)

    result_reports = spending_by_category(df, 'Супермаркеты', date_input)
    print(result_reports)