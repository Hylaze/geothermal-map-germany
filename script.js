var map = L.map('map', {
    center: [50.876903, 10.492287], // Mittelpunkt von Deutschland
    zoom: 6,  // Zoom-Level
    maxBounds: [
        [47.071840, 5.438576],  // Südwestliche Koordinaten (linke untere Ecke von Deutschland)
        [55.242990, 15.699807]   // Nordöstliche Koordinaten (rechte obere Ecke von Deutschland)
    ], 
    maxBoundsViscosity: 1.0 // Option, um das "Springen" der Karte an den Rand zu verhindern
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> - Hannah Zemlin',
    maxZoom: 18,
    minZoom: 5
}).addTo(map);

function createMarkerIcon(color) {
    return L.divIcon({
        className: 'custom-marker-icon',
        html: '<div style="background-color: ' + color + '; width: 16px; height: 16px; border-radius: 50%;"></div>',
        iconSize: [16, 16],
        iconAnchor: [8, 8],
        popupAnchor: [0, 0]
    });
}

var markers = {
    cities: [],
    geothermal: []
};

function loadMarkers() {
    fetch('marker.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(marker => {
                let markerColor;
                let markerIcon;
                let markerType;

                switch (marker.type) {
                    case 'betrieb':
                        markerColor = '#e81621';
                        markerType = 'cities';
                        break;
                    case 'planung':
                        markerColor = '#60bf59';
                        markerType = 'geothermal';
                        break;
                    default:
                        markerColor = 'gray';
                        markerType = 'cities';
                }

                markerIcon = createMarkerIcon(markerColor);
                let mapMarker = L.marker(marker.coords, { icon: markerIcon })
                    .bindPopup(`<b>${marker.name}</b><br>${marker.info}`)
                    .addTo(map);

                markers[markerType].push(mapMarker);
            });

            updateMarkersVisibility();
        })
        .catch(error => console.error('Fehler beim Laden der Marker:', error));
}

function updateMarkersVisibility() {
    let citiesVisible = document.getElementById('toggle-cities').checked;
    let geothermalVisible = document.getElementById('toggle-geothermal').checked;

    markers.cities.forEach(marker => {
        marker.setOpacity(citiesVisible ? 1 : 0);
    });

    markers.geothermal.forEach(marker => {
        marker.setOpacity(geothermalVisible ? 1 : 0);
    });
}

// Event listeners for checkboxes
document.getElementById('toggle-cities').addEventListener('change', updateMarkersVisibility);
document.getElementById('toggle-geothermal').addEventListener('change', updateMarkersVisibility);

// Load markers and initialize visibility
loadMarkers();
