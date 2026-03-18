var displayFeatureInfo = function (pixel) {
  var feature = map_obj.forEachFeatureAtPixel(pixel, function (feature) {
    return feature;
  });  
  if (feature) {
    console.log(feature.get('MvtSpeed'), feature.get('LatTrajCellCG'), feature.get('LonTrajCellCG'));
  }
};
     
map_obj.on('click', function (evt) {
  displayFeatureInfo(evt.pixel);
}); 