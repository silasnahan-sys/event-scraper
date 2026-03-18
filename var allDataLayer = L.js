var allDataLayer = L.geoJson(DCALayer, {
    pointToLayer: function (feature, OBJECTID) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
    },

    onEachFeature: function (feature, layer) {
        var popupcontent = [];
        for (var prop in feature.properties) {
            popupcontent.push(prop + ": " + feature.properties[prop]);
        }
        layer.bindPopup(popupcontent.join("<br />"));

    }

    var region; 

window.addEventListener('message', (event) => {
    if (event.data && event.data.action === 'sync-resize-fly') {
        const vc = event.data.vc;
        if (vc) {
            console.log("Searching for:", vc);
            runSearch(vc);
        }
    }
});

// Load your combined Somerville/Cambridge file
fetch('./somervilleNeighborhoods (2).geo.json') 
    .then(response => response.json())
    .then(data => {
        region = L.geoJSON(data, {
            style: { color: 'blue', weight: 2, fillOpacity: 0.1 }
        }).addTo(map);
    });

function runSearch(combinedData) {
    if (!region || !combinedData) return;

    // 1. Split the data back into the Name and the Address
    const parts = combinedData.split(" | ");
    const vTitle = parts[0];   // e.g., "Lou's"
    const vAddress = parts[1]; // e.g., "13 Brattle St., Cambridge, MA"

    // 2. Create the search query for the geocoder
    // We use the Address for searching because it's more reliable than the Name
    let searchQuery = vAddress;
    if (!searchQuery.toLowerCase().includes("ma")) searchQuery += ", MA";

    const provider = new window.GeoSearch.OpenStreetMapProvider();
    
    provider.search({ query: searchQuery }).then(results => {
        if (results.length === 0) {
            console.warn("Geosearch failed for address:", searchQuery);
            return;
        }

        const result = results[0]; 
        const latlng = L.latLng(result.y, result.x);
        
        let isInside = false;
        region.eachLayer(function(layer) {
            if (isInside) return;
            if (isMarkerInsidePolygon(latlng, layer)) isInside = true;
        });

        // 3. Create the marker with BOTH Venue Title and Address
        if (isInside) {
            map.flyTo(latlng, 17);
            L.marker(latlng).addTo(map)
               .bindPopup(`<strong>${vTitle}</strong><br>${vAddress}<br><em>(Near boundary)</em>` + feature.properties["OBJECTID)"]) // Bold Name, then Address
                .openPopup();
        } else {
      7      // Fallback for near-boundary hits
            map.flyTo(latlng, 17);
            L.circleMarker(latlng, {color: 'orange'}).addTo(map)
                .bindPopup(`<strong>${vTitle}</strong><br>${vAddress}<br><em>(Near boundary)</em>`)
                .openPopup();
        }
    });
}
// Robust Point-in-Polygon Math
function isMarkerInsidePolygon(latlng, poly) {
    const x = latlng.lat, y = latlng.lng;
    const json = poly.toGeoJSON();
    const type = json.geometry.type;
    const coords = json.geometry.coordinates;

    function checkRing(ring) {
        let inside = false;
        for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
            // ring[i][1] is Latitude, ring[i][0] is Longitude
            const xi = ring[i][1], yi = ring[i][0]; 
            const xj = ring[j][1], yj = ring[j][0];

            const intersect = ((yi > y) !== (yj > y)) &&
                (x < ((xj - xi) * (y - yi) / (yj - yi) + xi));
            if (intersect) inside = !inside;
        }
        return inside;
    }

    if (type === "Polygon") {
        return checkRing(coords[0]);
    } else if (type === "MultiPolygon") {
        // Essential for Cambridge neighborhoods which often have multiple parts
        return coords.some(p => checkRing(p[0]));
    }
    return false;
}


</script>

    </body>
</html>     

    // CONFIG: Fluidity settings
    map.options.zoomSnap = 0; 
    map.options.zoomDelta = 0.1;

    // SYNC: Matches your 0.8s CSS transition
    let startTime = performance.now();
    function syncExpansion(now) {
        map.invalidateSize({ animate: false, pan: false });
        if (map._renderer) map._renderer._update();
        if (now - startTime < 600) {
            requestAnimationFrame(syncExpansion);
        } else {
            map.invalidateSize();
            setTimeout(startLiquidFlight, 50);
        }
    }
    requestAnimationFrame(syncExpansion);

    function startLiquidFlight() {
        let targetLayer;
        
        // Find specific neighborhood if ID was sent
        if (requestedId) {
            neighborhoodLayer.eachLayer(layer => {
                
                if (layer.feature.properties && layer.feature.properties.OBJECTID === requestedId) {
                    targetLayer = layer;
                }
            });
        }

        // 6. THE FLIGHT: Fly to specific layer OR Full Map if ID is missing
        // neighborhoodLayer.getBounds() shows the entire city
        const bounds = targetLayer ? targetLayer.getBounds() : neighborhoodLayer.getBounds();
        
        map.flyToBounds(bounds, {
            padding: [40, 40],
            duration: 2.5,
            easeLinearity: 0.05,
            noMoveStart: true
        });

        // 7. THE ARRIVAL: Auto-activate the D3 path for the specific ID
        if (targetLayer) {
            map.once('moveend', () => {
                const d3Target = d3.selectAll("path.neighborhood")
                    .filter(d => d && d.properties && d.properties.OBJECTID === requestedId);
                
                if (!d3Target.empty()) {
                    const node = d3Target.node();
                    const handler = d3.select(node).on('click');
                    if (handler) handler.call(node, d3.select(node).datum());
                }
            });
        }
    }

