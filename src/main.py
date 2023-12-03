import os
from config import ROOT_DIR
from load_map_points import map_and_point
from pull_static_mobilithek import pull_and_save_data
from visualiser import plot_basemap

reload_data = False


def main():
    filename = "default.csv"
    if reload_data:
        path = os.path.join(ROOT_DIR, "data")
        filename = pull_and_save_data(path)
    map_and_point(filename)
    plot_basemap()


if __name__ == '__main__':
    main()
