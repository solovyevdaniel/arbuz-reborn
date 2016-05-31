/**
 * Created by admin on 04.09.2015.
 */
var data = [];

var currMap = {};

var map, heatmap, markers, directionsService, directionsDisplay, query, CrimeList, mc;

function CenterControl(controlDiv, map) {

    // Set CSS for the control border.
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginTop = '10px';
    controlUI.style.overflow = 'hidden';
    controlUI.style.textAlign = 'center';
    controlUI.userSelect = "none";
    controlUI.webkitUserSelect = "none";
    controlUI.MozUserSelect = "none";
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.userSelect = "none";
    controlText.webkitUserSelect = "none";
    controlText.MozUserSelect = "none";
    controlText.innerHTML =
        '<input id="turnOnMarker" class="cmn-toggle" type="radio" name="mapeType" checked>' +
        '<label for="turnOnMarker" onclick="turnOnMarkers();turnOffHeatmap()" class="mapControl">' +
        '<span>Маркери</span>' +
        '</label>' +
        '<input id="turnOnHeatmap" class="cmn-toggle" type="radio" name="mapeType">' +
        '<label for="turnOnHeatmap" onclick="turnOnHeatmap();turnOffMarkers()" class="mapControl">' +
        '<span">Градієнт</span>' +
        '</label>';
    controlUI.appendChild(controlText);

    // Setup the click event listeners: simply set the map to Chicago.

}

function LeftControl(controlDiv, map) {
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginTop = '10px';
    controlUI.id = 'leftControl';
    controlUI.style.overflow = 'hidden';
    controlUI.style.textAlign = 'center';
    controlUI.userSelect = "none";
    controlUI.webkitUserSelect = "none";
    controlUI.MozUserSelect = "none";
    controlDiv.appendChild(controlUI);

    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.userSelect = "none";
    controlText.webkitUserSelect = "none";
    controlText.MozUserSelect = "none";
    controlText.innerHTML =
        '<label onclick="" class="mapControl">' +
        '<span><img src="/static/glyphicons-42-charts.png" /></span>' +
        '</label>' +
        '<label onclick="toggleSidebar()" class="mapControl">' +
        '<span><img src="/static/office2.png" /></span>' +
        '</label>';
    controlUI.appendChild(controlText);
}

function initMap() {
    // Parse.initialize('XDBnSlerhSroUGtZ4pqJEzv7TFpNMPhIZPtRF9Fm', '7pG4HYMKkCRCtwUKShrOKsEt5STyUfIhGYqXwjRi');
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DEFAULT,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        center: {
            lat: 50.42897117935071,
            lng: 30.509033203125
        },
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });
    currMap = map;
    directionsDisplay.setMap(map);

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map,
        radius: 125
    });

    var centerControlDiv = document.createElement('div');
    var centerControl = new CenterControl(centerControlDiv, map);

    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);

    var leftControlDiv = document.createElement('div');
    var leftControl = new LeftControl(leftControlDiv, map);

    leftControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(leftControlDiv);


    // CrimeList = Parse.Object.extend("streets");
    // query = new Parse.Query(CrimeList);
    // query.equalTo('month', 3);
    //query.equalTo('total_points', 0);
    var offset = 0;

    // var interval = setInterval(function () {
    //     query.skip(offset);
    //     query.find({
    //         success: function (crimeList) {
    //             //Parse.Object.destroyAll(crimeList);
    //             offset+=100;
    //             data = data.concat(crimeList);
    //             heatmap.setData(getPoints());
    //             for (var i = offset-100; i < data.length; i++) {
    //                 markers.push(new google.maps.Marker({
    //                     position: new google.maps.LatLng(data[i].attributes.location.latitude, data[i].attributes.location.longitude),
    //                     map: currMap
    //                 }));
    //                 markers[markers.length-1].addListener('click', function() {
    //                     var infowindow = new google.maps.InfoWindow({
    //                         content: getContentString(data[i].attributes),
    //                         maxWidth: 200
    //                     });
    //                     infowindow.open(map, this);
    //                 });
    //             }
    //             if (crimeList.length < 100){
    //                 clearInterval(interval)
    //             }
    //             //clearInterval(interval)
    //         },
    //         error: function (object, error) {
    //             clearInterval(interval)
    //         }
    //     });
    // }, 1000);

    $.getJSON('buildings', function (buildings) {
        for (var i = 0; i < buildings.length; i++) {
            if (buildings[i].crimes[0].total == 0 || buildings[i].crimes[0].total_points == 0){
                buildings.splice(i, 1);
                i--;
            }
        }
        data = buildings;
        heatmap.setData(getPoints());
        for (var i = 0; i < data.length; i++) {
            markers.push(new google.maps.Marker({
                position: new google.maps.LatLng(data[i].latitude, data[i].longitude),
                map: currMap
            }));
            (function (building) {
                markers[markers.length - 1].addListener('click', function () {
                    var infowindow = new google.maps.InfoWindow({
                        content: getContentString(building.crimes[0]),
                        maxWidth: 200
                    });
                    infowindow.open(map, this)
                });
            })(data[i]);
        }
        mc = new MarkerClusterer(currMap, markers,
            {
                maxZoom: 13,
                gridSize: 50,
                styles: null
            });
    });

    google.maps.event.addListener(map, 'click', function (event) {
        var myLatLng = event.latLng;
        console.log(myLatLng.lat(), myLatLng.lng());
        console.log(map.getZoom());
        // markers.push(new google.maps.Marker({
        //     position: new google.maps.LatLng(myLatLng.lat(), myLatLng.lng()),
        //     map: map,
        //     icon: 'http://gmapsmarkergenerator.eu01.aws.af.cm/getmarker?scale=1&color=ffff00'
        // }));
    });

    markers = [];
    turnOnMarkers();
    turnOffHeatmap();
}

function getContentString(crime) {
    var str = '<ul style="list-style: none">' +
        (crime.heav_osobo_heav > 0 ? '<li><span>Тяжкі та о.тяжкі:</span><span>' + crime.heav_osobo_heav + '</span></li>' : '') +
        (crime.murder > 0 ? '<li><span>Вбивства:</span><span>' + crime.murder + '</span></li>' : '') +
        (crime.intentional_injury > 0 ? '<li><span>Умисне тяж тіл ушкодження:</span><span>' + crime.intentional_injury + '</span></li>' : '') +
        (crime.bodily_harm_with_fatal_cons > 0 ? '<li><span>Тяж тіл ушкодж зі смерт. насл:</span><span>' + crime.bodily_harm_with_fatal_cons + '</span></li>' : '') +
        (crime.rape > 0 ? '<li><span>Згвалтування:</span><span>' + crime.rape + '</span></li>' : '') +
        (crime.theft > 0 ? '<li><span>Крадіжка:</span><span>' + crime.theft + '</span></li>' : '') +
        (crime.looting > 0 ? '<li><span>Грабіж:</span><span>' + crime.looting + '</span></li>' : '') +
        (crime.brigandage > 0 ? '<li><span>Розбій:</span><span>' + crime.brigandage + '</span></li>' : '') +
        (crime.extortion > 0 ? '<li><span>Вимагання:</span><span>' + crime.extortion + '</span></li>' : '') +
        (crime.fraud > 0 ? '<li><span>Шахрайство:</span><span>' + crime.fraud + '</span></li>' : '') +
        (crime.hooliganism > 0 ? '<li><span>Хулігантство:</span><span>' + crime.hooliganism + '</span></li>' : '') +
        (crime.drugs > 0 ? '<li><span>Наркотики:</span><span>' + crime.drugs + '</span></li>' : '') +
        '</ul>'
    return str;
}

var rat;

function calcRoute() {
    var start = document.getElementById("origin").value;
    var end = document.getElementById("destination").value;
    var request = {
        origin: start,
        destination: end,
        travelMode: google.maps.TravelMode.WALKING,
        provideRouteAlternatives: true
    };
    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            result.routes[0] = findSafeRoute(result.routes);
            directionsDisplay.setDirections(result);
            document.getElementById('dist').innerHTML = result.routes[0].legs[0].distance.text;
            document.getElementById('dur').innerHTML = result.routes[0].legs[0].duration.text;
            document.getElementById('rat').innerHTML = Math.round(rat);
        }
    });
}

function findSafeRoute(routes) {
    var ratings = [];
    for (var i = 0; i < routes.length; i++) {
        ratings[i] = getSafeRating(routes[i].overview_path) / routes[i].legs[0].distance.value * 100;
    }
    var min = Number.MAX_VALUE;
    var min_route;
    for (i = 0; i < ratings.length; i++) {
        if (ratings[i] < min) {
            min = ratings[i];
            min_route = routes[i];
        }
    }
    rat = min;
    return min_route;
}

function distanceSqr(x1, y1, x2, y2) {
    return (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1);
}

function getSafeRating(points) {
    var res = [];
    for (var i = 0; i < points.length; i++) {
        var point = points[i];
        var ERR = 0.002;
        for (var j = 0; j < data.length; j++) {
            var crime = data[j];
            var d = distanceSqr(point.G, point.K, crime.latitude, crime.longitude)
            if (d < ERR * ERR) {
                res.push(
                    (crime.bodily_harm_with_fatal_cons * 5 +
                    crime.brigandage * 3 +
                    crime.drugs * 3 +
                    crime.extortion * 2 +
                    crime.fraud * 1 +
                    crime.heav_osobo_heav * 5 +
                    crime.hooliganism * 1 +
                    crime.intentional_injury * 4 +
                    crime.looting * 2 +
                    crime.murder * 5 +
                    crime.rape * 4 +
                    crime.theft * 1) * (1 - d / (ERR * ERR))
                )
            }
        }
    }
    var sum = 0;
    for (i = 0; i < res.length; i++) {
        sum += res[i];
    }
    return sum;
}

function toggleMap() {
    currMap = currMap ? null : map;
    //setTimeout(function () {
    toggleHeatmap();
    //}, 0);
    toggleMarkers();
}

function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
}

function toggleSidebar() {
    var element = document.querySelector('.sidebar');
    element.classList.toggle('visible');
    element = document.querySelector('#leftControl');
    element.classList.toggle('visible');
}

function changeRadius() {
    heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
    heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

function getPoints() {
    return data.map(function (item) {
        return new google.maps.LatLng(item.latitude, item.longitude)
    });
}

function toggleMarkers() {
    if (mc.getMarkers().length){
        mc.clearMarkers();
    } else {
        mc.addMarkers(markers);
    }
}

function turnOnMarkers() {
    if (mc && mc.getMarkers().length == 0){
        mc.addMarkers(markers);
    }
}

function turnOffMarkers() {
    mc.clearMarkers();
}

function turnOnHeatmap() {
    heatmap.setMap(map);
}

function turnOffHeatmap() {
    heatmap.setMap(null);
}