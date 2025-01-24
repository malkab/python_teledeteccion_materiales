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
        <paletteEntry value="0" color="#5977cc" alpha="255" label="Pantano"/>
        <paletteEntry value="1" color="#2c49a0" alpha="255" label="Océano"/>
        <paletteEntry value="2" color="#ababab" alpha="255" label="Suelo / urbano"/>
        <paletteEntry value="3" color="#c0dfff" alpha="255" label="Aguas litorales"/>
        <paletteEntry value="4" color="#627b4c" alpha="255" label="Vegetación vigorosa"/>
        <paletteEntry value="5" color="#ffcc00" alpha="255" label="Arena"/>
        <paletteEntry value="6" color="#005b3f" alpha="255" label="Marisma"/>
        <paletteEntry value="7" color="#a7d22d" alpha="255" label="Vegetación rala"/>
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
