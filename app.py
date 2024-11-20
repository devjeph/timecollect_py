""" app.py """
import services.google_api as services
import utils.data_collection as utils


def main():
    """ function that will connect to Google Sheet API"""
    services.sheet_service()
    value = utils.run_data('1gBCnhREhrI8WmClCXkOxpRhn7T97Qics1Ori3cev0ss', "202411!A7:AT39")
    print(len(value))


if __name__ == '__main__':
    main()
    