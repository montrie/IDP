import os
from config import ROOT_DIR
from load_map_points import map_and_point
from pull_static_mobilithek import pull_and_save_data_static
from pull_xml_to_csv_mobilithek import pull_and_save_data_xml
from visualiser import plot

reload_data = True


def main():
    filename_static = "default.csv"
    if reload_data:
        path_static = os.path.join(ROOT_DIR, "static_data")
        path_xml = os.path.join(ROOT_DIR, "xml_data")
        filename_static = pull_and_save_data_static(path_static)
        filename_xml = pull_and_save_data_xml(path_xml)

    map_and_point(filename_static)
    plot()


if __name__ == '__main__':
    main()
