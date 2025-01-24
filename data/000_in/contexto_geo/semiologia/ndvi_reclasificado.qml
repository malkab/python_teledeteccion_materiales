<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40.3-Bratislava" styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|Diagrams|GeometryOptions|Relations|Legend">
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option name="name" value="" type="QString"/>
      <Option name="properties"/>
      <Option name="type" value="collection" type="QString"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer opacity="1" band="1" alphaBand="-1" nodataColor="" type="paletted">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry value="0" color="#a6cee3" alpha="255" label="Agua"/>
        <paletteEntry value="1" color="#e4e4e4" alpha="255" label="Urbano / suelo desnudo"/>
        <paletteEntry value="2" color="#b4a21a" alpha="255" label="Vegetación rala"/>
        <paletteEntry value="3" color="#005e2a" alpha="255" label="Vegetación vigorosa"/>
        <paletteEntry value="4" color="#77ee38" alpha="255" label="Vegetación muy vigorosa"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors">
        <Option/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation colorizeRed="255" invertColors="0" colorizeGreen="128" colorizeStrength="100" colorizeOn="0" colorizeBlue="128" saturation="0" grayscaleMode="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
