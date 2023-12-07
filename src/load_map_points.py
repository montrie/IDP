# from PyQt5.QtCore import QTimer
import os
from qgis.core import *
from qgis._gui import QgsMapCanvas
from config import ROOT_DIR
from qgis.utils import iface

"""
system-specific parameters, change to reflect
ROOT_DIR: root directory of the code base
prefix_path: path to root directory of QGIS installation
tms: link to a basemap from OpenStreetMaps
absolute_path_to_csv_file: absolute path to local csv file containing detector static_data
options: options for loading the detector static_data
options2: TBD
csv_uri: final URI of the detector static_data csv file
project_location: path of the created QGIS project file 
"""
ROOT_DIR = os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-1])
prefix_path = "D:\Program Files\QGIS 3.32.3"
tms = 'crs=EPSG:3857&type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
absolute_path_to_csv_file = os.path.join(ROOT_DIR, "static_data")
options = '?delimiter=,&xField=lon&yField=lat&crs=epsg:4326'
options2 = '?type=csv&amp;delimiter=,&amp;xField=lon&amp;yField=lat&amp;crs=EPSG:4326&amp;'
project_location = os.path.join(ROOT_DIR, "project_files")


def print_layer_error(layer):
    """ Print a summary of the error stored in ``layer``

    :param layer: A valid Qgs Layer
    """
    print("Failed to load layer!\n{}".format(layer.error().summary()))


def set_project_crs():
    """
    This method sets the CRS (coordinate reference system) of the QgsPoject instance
    """
    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:3857'))


def map_and_point(data_file_name: str = "default.csv") -> QgsProject:
    """Load a base map from OSM and the detector static_data from the static_data stored in ``data_file_name``,
    add them a QgsProject instance, write the .qgs file to disk and return the QgsProject object

    :param data_file_name: File name of the detector static_data
    :return: Object of the QgsProject
    """
    QgsApplication.setPrefixPath(prefix_path, True)
    qgs = QgsApplication([], True)
    project = QgsProject.instance()

    # Load another project
    # project.read('mapping_muc_loops.qgz')
    qgs.initQgis()

    # Adding Map
    rlayer = QgsRasterLayer(tms, 'OSM', 'wms')
    if rlayer.isValid():
        project.addMapLayer(rlayer)
        set_project_crs()
    else:
        print_layer_error(rlayer)

    # Adding Points
    csv_uri = "file:///{}{}".format(os.path.join(absolute_path_to_csv_file, data_file_name), options)
    csvlayer = QgsVectorLayer(csv_uri, "Points", "delimitedtext")
    if csvlayer.isValid():
        project.addMapLayer(csvlayer)
        # https://gis.stackexchange.com/questions/303704/project-crs-not-being-respected-by-qgis/303710#303710:~:text=%23%20Call%20QTimer%20with%2010ms%20delay%20(adjust%20to%20suit)%20to%20set%20CRS
        # QTimer.singleShot(10, set_project_crs)
        csvlayer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
    else:
        print_layer_error(csvlayer)

    # Fit rlayer to screen and refresh the canvas
    canvas = QgsMapCanvas()
    canvas.setCurrentLayer(rlayer)
    canvas.setExtent(rlayer.extent())
    canvas.refresh()

    project.write(filename=os.path.join(project_location, data_file_name.split(".")[0] + ".qgs"))

    print("Map and detector points have been loaded: " + os.path.join(project_location, project.fileName()))

    return project
