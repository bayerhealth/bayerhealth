if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(setLocation);
}

function fillForm() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setLocation);
    }
}

function setLocation(position) {
    var latField = document.getElementById("lat");
    var lngField = document.getElementById("lng");
    latField.value = position.coords.latitude;
    lngField.value = position.coords.longitude;
}