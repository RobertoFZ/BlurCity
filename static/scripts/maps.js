var markerArray = [];
var wayPoints = [];
var markerPosition = 1;
var googleMarkersArray = [];
var route_ok = false;

var directionsService;
var directionsDisplay;
var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: {lat: 41.85, lng: -87.65}
    });
    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer;
    directionsDisplay.setMap(map);
    var infoWindow = new google.maps.InfoWindow({map: map});

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
        var markerObject = {
            position: markerPosition,
            latitud: newMarker.getPosition().lat(),
            longitud: newMarker.getPosition().lng()
        };
        markerArray.push(markerObject);
        googleMarkersArray.push(newMarker);
        markerPosition++;
    });

    $('#clean-btn').on("click", function () {
        deleteMarkers();
        directionsDisplay.setMap(null);
    });
}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    destination = "";

    campus_pk = document.getElementById('destiny').value;
    for (var i = 0; i < campus_list.length; i++) {
        if (campus_list[i].pk == campus_pk) {
            destination = campus_list[i].points;
            var markerObject = {
                position: markerPosition++,
                latitud: campus_list[i].latitude,
                longitud: campus_list[i].longitude
            };
            markerArray.push(markerObject);
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
    directionsDisplay.setMap(map);
    route_ok = true;
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
        if (origen != "" && destino != "" && vehiculo != "" && cupo != "" && horario != "" && route_ok) {
            $.ajax({
                url: '/panel/save_route/',  //Server script to process data
                type: 'post',
                success: function (data) {
                    console.log(data);
                    if (data != "-1") {
                        routeId = data;
                        console.log("ID RUTA AJAX " + routeId);
                        console.log(markerArray);
                        if (markerArray.length > 0) {
                            for (var i = 0; i < markerArray.length; i++) {
                                $.ajax({
                                    url: '/panel/save_markers/',  //Server script to process data
                                    type: 'post',
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
                            Materialize.toast('Ruta guardada correctamente', 10000, 'rounded')
                        } else {
                            sweetAlert("Error", "Por favor trace una ruta", "error");
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
            if (!route_ok) {
                sweetAlert("Error", "Por favor traze la ruta y asegurese que es la correcta", "error");
            } else {
                sweetAlert("Error", "Por favor llene todos los campos", "error");
            }
        }
    } else {
        sweetAlert("Error", "Por favor seleccione el dia de la semana que estará disponible esta ruta", "error");
    }
}

function deleteMarker(markerToDelete) {
    var temp_marker_array = [];
    var temp_wayPoints = [];
    var temp_googleMarkersArray = [];

    for (var i = 0; i < markerArray.length; i++) {
        if (markerArray[i].latitud != markerToDelete.getPosition().lat() && markerArray[i].longitud != markerToDelete.getPosition().lng()) {
            temp_marker_array.push(markerArray[i]);
            temp_wayPoints.push(wayPoints[i]);
            temp_googleMarkersArray.push(googleMarkersArray[i]);
        } else {
            console.log("Marker to delete found");
        }
    }

    wayPoints = temp_wayPoints;
    markerArray = temp_marker_array;
    googleMarkersArray = temp_googleMarkersArray;
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    if (!route_ok) {
        for (var i = 0; i < markerArray.length; i++) {
            googleMarkersArray[i].setMap(map);
        }
    } else {
        for (var i = 0; i < markerArray.length - 1; i++) {
            googleMarkersArray[i].setMap(map);
        }
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
    googleMarkersArray = [];
    route_ok = false;
}
