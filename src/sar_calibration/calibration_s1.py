import os
from snapista import Graph, Operator

os.environ['_JAVA_OPTIONS'] = '-Xms24g -Xmx24g'

def get_identifier(safe):

    return os.path.basename(os.path.dirname(safe)).replace(".SAFE", "")
    

def graph_calibrate_s1(safe):
    
    identifier = get_identifier(safe)
    
    g = Graph()

    g.add_node(
        operator=Operator("Read", formatName="SENTINEL-1", file=f"{safe}"), 
        node_id="read")

    print("Node: Apply-Orbit-File")

    g.add_node(
        operator=Operator("Apply-Orbit-File", continueOnFail="true"),
        node_id="apply-orbit-file",
        source="read",
    )

    print("Node: Remove-GRD-Border-Noise")

    g.add_node(
        operator=Operator("Remove-GRD-Border-Noise", borderLimit="2000", trimThreshold="0.2"),
        node_id="noise-removal",
        source="apply-orbit-file",
    )

    print("Node: Calibration")

    g.add_node(
        operator=Operator("Calibration", selectedPolarisations="VV"),
        node_id="calibration",
        source="noise-removal",
    )

    print("Node: LinearToFromdB")

    g.add_node(
        operator=Operator("LinearToFromdB", sourceBandNames="Sigma0_VV"),
        node_id="linear",
        source="calibration",
    )

    print("Node: Terrain-Correction")

    g.add_node(
        operator=Operator(
            "Terrain-Correction", pixelSpacingInMeter="20.0", demName="SRTM 1Sec HGT"
        ),
        node_id="terrain-correction",
        source="linear",
    )
    
    print("Node: Subset")

    g.add_node(
        operator=Operator("Subset", copyMetadata = True, geoRegion='POLYGON((12.767154479927116 41.73189894469486,12.844058776802116 41.73189894469486,12.844058776802116 41.68063637079049,12.767154479927116 41.68063637079049,12.767154479927116 41.73189894469486))'),
        node_id="subset",
        source="terrain-correction",
    )
    
    print("Node: Write")

    g.add_node(
        operator=Operator("Write", file=f"{identifier}_SIGMA0_VH_DB", formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="subset",
    )

    return g
