var googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

var mymap = L.map('mapid')
var mylat;
var mylng;
var currTileLayer = 'Streets';
var myMarkers = L.layerGroup();

googleStreets.addTo(mymap);

function addCurrentLocation(lat, lng){
    mylat = lat;
    mylng = lng
    mymap.setView([mylat, mylng], 16);
                 
    var marker = L.marker([mylat, mylng]).bindPopup("Tu jesteś").addTo(mymap);
    // show('Siłownia');
}

function getMyPosition() {
    navigator.geolocation.getCurrentPosition(position => addCurrentLocation(position.coords.latitude, position.coords.longitude),
					 error => addCurrentLocation(52.219761, 21.002734));
}

function changeMapView() {
    if (currTileLayer === 'Streets') {
        mymap.removeLayer(googleStreets);
        googleSat.addTo(mymap);
        // console.log('to sat');
        currTileLayer = 'Sat';
    }
    else if (currTileLayer === 'Sat') {
        mymap.removeLayer(googleSat);
        googleStreets.addTo(mymap);
        // console.log('to str');
        currTileLayer = 'Streets';
    }
}

// Buttons

L.easyButton('fas fa-map', function(btn, map){
    changeMapView();
}).addTo(mymap);

L.easyButton('fas fa-map-marker-alt', function(btn, map){
    getMyPosition();
}).addTo(mymap);


// var gym = L.icon({
//     iconUrl: 'static/pics/gym.svg',
//     iconSize: [20, 40],
//     iconAnchor: [10, 0],
//     popupAnchor: [0, 0],
// });

// var person = L.icon({
//     iconUrl: 'static/pics/person.svg',
//     iconSize: [20, 40],
//     iconAnchor: [10, 0],
//     popupAnchor: [0, 0],
// });

// var bike = L.icon({
//     iconUrl: 'static/pics/bike.svg',
//     iconSize: [20, 40],
//     iconAnchor: [10, 0],
//     popupAnchor: [0, 0],
// });

// var swim = L.icon({
//     iconUrl: 'static/pics/swim.svg',
//     iconSize: [20, 40],
//     iconAnchor: [10, 0],
//     popupAnchor: [0, 0],
// });

// var forest = L.icon({
//     iconUrl: 'static/pics/forest.svg',
//     iconSize: [20, 40],
//     iconAnchor: [10, 0],
//     popupAnchor: [0, 0],
// });

// var pitch = L.icon({
//     iconUrl: 'static/pics/pitch.svg',
//     iconSize: [20, 40],
//     iconAnchor: [10, 0],
//     popupAnchor: [0, 0],
// });



//Filtry
// L.easyButton('fas fa-dumbbell', function(button, map){show('Siłownia')} ).addTo(mymap);
// L.easyButton('fas fa-futbol', function(button, map){show('Boisko')} ).addTo(mymap);
// L.easyButton('fas fa-swimmer', function(button, map){show('Basen')} ).addTo(mymap);
// L.easyButton('fas fa-bicycle', function(button, map){show('Rowery')} ).addTo(mymap);
// //L.easyButton('fas fa-tree', function(button, map){show('Park')} ).addTo(mymap);
// L.easyButton('fas fa-redo', function(button, map){show(null)} ).addTo(mymap);
// L.easyButton('fas fa-male', function(button, map){myView()} ).addTo(mymap);

// //Wypisywanie obiektow
// function show(filter){
//         mymap.removeLayer(myMarkers);
//         myMarkers = L.layerGroup();
//         for(var i = 0; i < objects.length; i++) {
//             var obj = objects[i];
//             var type = obj[1];

//             if(filter != null && type != filter){
//                 continue;
//             } else{
//                 var id = obj[0];
//                 var lat = obj[2];
//                 var lng = obj[3];
//                 switch (type) {
//                     case 'Siłownia':
//                         addMarker(gym, lat, lng, id)
//                         break;
//                     case 'Boisko':
//                         addMarker(pitch, lat, lng, id)
//                         break;
//                     case 'Rowery':
//                         addMarker(bike, lat, lng, id)
//                         break;
//                     case 'Basen':
//                         addMarker(swim, lat, lng, id)
//                         break;
//                     case 'Park':
//                         addMarker(forest, lat, lng, id)
//                         break;
//                     default:
//                         addMarker(gym, lat, lng, id)
//                         break;
//             }  
//         }
             
//     } 
//     myMarkers.addTo(mymap);  
// }





// function encodeQueryData(data) {
//    const ret = [];
//    for (let d in data)
//      ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
//    return ret.join('&');
// }

// function addMarker(type, lat, lng, id) {

//     var marker = L.marker([lat, lng], {icon: type})
//     var data = {'id' : id};
//     marker.url = '/gym?'+encodeQueryData(data);
//     marker.on('click', function(){
//         window.location = (this.url);
//     });
//     marker.addTo(myMarkers);
// }


getMyPosition();