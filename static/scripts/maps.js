var markerArray = [];
var wayPoints = [];
var markerPosition = 1;
var googleMarkersArray = [];

function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: {lat: 41.85, lng: -87.65}
    });
    directionsDisplay.setMap(map);

    var infoWindow = new google.maps.InfoWindow({map: map});
    var route_ok = false;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        handleLocationError(false, infoWindow, map.getCenter());
    }

    var onChangeHandler = function () {
        //setMapOnAll(null);

        //TODO: Ajax Request for save data in Database
        //sendRouteDataToServer();
        calculateAndDisplayRoute(directionsService, directionsDisplay);
        route_ok = true;
    };

    document.getElementById('draw-btn').addEventListener('click', onChangeHandler);
    document.getElementById('guardar-btn').addEventListener('click', sendRouteDataToServer);

    map.addListener('click', function (click) {
        var newMarker = new google.maps.Marker({
            position: click.latLng,
            map: map,
            title: 'Marcador'
        });
        newMarker.addListener('click', function () {
            newMarker.setVisible(false);
            deleteMarker(newMarker);
        });
        wayPoints.push({
            location: newMarker.getPosition(),
            stopover: false
        });
        //markerArray.push(newMarker);
        var markerObject = {
            position: markerPosition,
            latitud: newMarker.getPosition().lat(),
            longitud: newMarker.getPosition().lng()
        };
        markerArray.push(markerObject);
        googleMarkersArray.push(newMarker);
        markerPosition++;
        console.log(markerArray);
    });

    $('#clean-btn').on("click", function () {
        deleteMarkers();
    });

}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    destination = "";

    campus_pk = document.getElementById('destiny').value;
    for (var i = 0; i < campus_list.length; i++) {
        if (campus_list[i].pk == campus_pk) {
            destination = campus_list[i].points;
            console.log(destination)
        }
    }

    directionsService.route({
        origin: wayPoints[0].location,
        destination: destination,
        waypoints: wayPoints,
        travelMode: google.maps.TravelMode.DRIVING
    }, function (response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });

}

function sendRouteDataToServer() {
    var dias = [];

    var origen = $('#origen').val();
    var destino = $('#destiny').val();
    var vehiculo = $('#car').val();
    var cupo = $('#sits').val();
    var horario = $('#hora').val();

    $('input[name="dia[]"]:checked').each(function () {
        dias.push($(this).val());
    });

    if ($('input[name="dia[]"]:checked').length > 0) {
        if (origen != "" && destino != "" && vehiculo != "" && cupo != "" && horario != "") {
            $.ajax({
                url: '/panel/save_route/',  //Server script to process data
                type: 'post',
                //Ajax events
                success: function (data) {
                    console.log(data);
                    if (data != "-1") {
                        routeId = data;
                        console.log("ID RUTA AJAX " + routeId);
                        console.log(markerArray);
                        for (var i = 0; i < markerArray.length; i++) {
                            $.ajax({
                                url: '/panel/save_markers/',  //Server script to process data
                                type: 'post',
                                //Ajax events
                                success: function (data) {
                                    console.log(data);
                                    deleteMarkers();
                                },
                                error: function (message) {
                                    console.log(message);
                                },
                                // Form data
                                data: {
                                    'routePk': routeId,
                                    'position': markerArray[i].position,
                                    'latitude': markerArray[i].latitud,
                                    'longitude': markerArray[i].longitud
                                }
                            });
                        }

                    }
                },
                error: function (message) {
                    console.log(message);
                },
                // Form data
                data: {
                    'origen': origen,
                    'destiny': destino,
                    'car': vehiculo,
                    'sits': cupo,
                    'time': horario,
                    'day': dias
                }
            });
        } else {
            alert("Por favor llene todos los campos");
        }
    } else {
        alert("Por favor seleccione el dia de la semana que estará disponible esta ruta");
    }
}

function deleteMarker(markerToDelete) {
    var temp_marker_array = [];
    var temp_wayPoints = [];

    for (var i = 0; i < markerArray.length; i++) {
        if (markerArray[i].latitud != markerToDelete.getPosition().lat() && markerArray[i].longitud != markerToDelete.getPosition().lng()) {
            temp_marker_array.push(markerArray[i]);
            temp_wayPoints.push(wayPoints[i]);
        } else {
            console.log("Marker to delete found");
        }
    }

    wayPoints = temp_wayPoints;
    markerArray = temp_marker_array;
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markerArray.length; i++) {
        googleMarkersArray[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markerArray = [];
    wayPoints = [];
}
