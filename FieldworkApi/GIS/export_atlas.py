import sys
import os
import platform
from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, QgsLayoutExporter, QgsLayoutItemMap

# --- 1️⃣ Configuratie QGIS-paden per OS ---
if platform.system() == "Darwin":  # macOS
    QGIS_APP = "/Applications/QGIS-LTR.app"
    QGIS_PREFIX = f"{QGIS_APP}/Contents/MacOS"
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["PROJ_LIB"] = f"{QGIS_APP}/Contents/Resources/proj"
    os.environ["GDAL_DATA"] = f"{QGIS_APP}/Contents/Resources/gdal"
elif platform.system() == "Windows":
    QGIS_APP = "C:/OSGeo4W/apps/qgis"
    QGIS_PREFIX = f"{QGIS_APP}"
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["PROJ_LIB"] = f"{QGIS_APP}/share/proj"
    os.environ["GDAL_DATA"] = f"{QGIS_APP}/share/gdal"
else:
    # Linux / ander
    QGIS_PREFIX = "/usr"
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

# --- 2️⃣ Input arguments ---
# argv[1] = path naar GeoJSON
# argv[2] = output map
if len(sys.argv) < 3:
    print("Usage: python export_atlas.py <geojson> <output_folder>")
    sys.exit(1)

geojson_path = sys.argv[1]
output_folder = sys.argv[2]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# --- 3️⃣ Start QGIS ---
QgsApplication.setPrefixPath(QGIS_PREFIX, True)
qgs = QgsApplication([], False)
qgs.initQgis()

# --- 4️⃣ Laad project ---
project = QgsProject.instance()
project_path = os.path.join(os.getcwd(), "project.qgz")
print("Project pad:", project_path)
ok = project.read(project_path)
print("Project geladen:", ok)
layer_name = "contour"  # naam zoals in project
layer = QgsVectorLayer(geojson_path, layer_name, "ogr")

layers = project.mapLayersByName("contour")

if len(layers) == 0:
    print("Contour layer niet gevonden in project!")
    sys.exit(1)

contour_layer = layers[0]

# datasource vervangen door je GeoJSON
contour_layer.setDataSource(
    geojson_path,
    "contour",
    "ogr"
)

print("Contour datasource vervangen")
for l in project.mapLayers().values():
    print(l.name())

# --- 6️⃣ Loop over layouts en export ---
for layout in project.layoutManager().layouts():
    print(f"Exporting layout: {layout.name()}")
    output_pdf = os.path.join(output_folder, f"{layout.name()}.pdf")
    output_jpg = os.path.join(output_folder, f"{layout.name()}.jpg")
    atlas = layout.atlas()
    atlas.setEnabled(True)
    atlas.setCoverageLayer(layer)
    atlas.beginRender()

    # Atlas-zoom instellen op alle map items
    for item in layout.items():
        if isinstance(item, QgsLayoutItemMap):
            item.setAtlasDriven(True)

    exporter = QgsLayoutExporter(layout)
    exporter.exportToPdf(output_pdf, QgsLayoutExporter.PdfExportSettings())
    exporter.exportToImage(output_jpg, QgsLayoutExporter.ImageExportSettings())

    atlas.endRender()

# --- 7️⃣ Exit QGIS ---
qgs.exitQgis()
print("Atlas export klaar ✅")