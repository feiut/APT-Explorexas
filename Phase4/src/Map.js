import React, { Component } from 'react';
import { StyleSheet, Text, View, Platform, FlatList, Alert, PermissionsAndroid} from 'react-native';
import Geolocation from 'react-native-geolocation-service';
import MapView, { PROVIDER_GOOGLE, Marker, Callout, Image, Circle } from 'react-native-maps'; // remove PROVIDER_GOOGLE import if not using Google Maps

export async function request_location_runtime_permission() {

  try {
      const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        'title': 'ReactNativeCode Location Permission',
        'message': 'ReactNativeCode App needs access to your location '
      }
    )
    if (granted === PermissionsAndroid.RESULTS.GRANTED) {
      Alert.alert("Location Permission Granted.");
    }
    else {
      Alert.alert("Location Permission Not Granted");
    }
  } catch (err) {
    console.warn(err)
  }
}

export default class Map extends Component {
     static navigationOptions =
     {
        title: 'View Reports on Map',
     };

     constructor(){
        super();
        this.state = {
            latitude: 0,
            longitude: 0,
            ready : false,
            isLoading : true,
            dataSource : []
        };
     }

     async componentDidMount(){
      var that = this;
      await request_location_runtime_permission();
      Geolocation.getCurrentPosition(
      position => {
        console.log("Current Location", position);
        var newLocation = JSON.stringify(position);
        var myLatitude = position.coords.latitude;
        console.log("Current latitude", myLatitude);
        var myLongitude = position.coords.longitude;
        console.log("Current longitude", myLongitude);
        this.setState({ latitude: myLatitude,
                        longitude: myLongitude,
                        ready: true
        });
      },
      error => Alert.alert(error.message),
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
    );

      return fetch('http://apt-team7.appspot.com/findReports', {
        method: "GET",
        headers:{
            'User-agent': Platform.OS
        }
      })
      .then(function(res){
        res.json().then(function(data) {
          console.log(data);
          that.setState({
            isLoading: false,
            dataSource : data,
          }, function(){
          });
        }).catch(function(error) {
          console.log('Map Data failed', error)
        });
    }).catch(function(error){
        console.log('Map request failed', error)
    })
     }

    render(){
        return(
             <MapView
                   provider={PROVIDER_GOOGLE} // remove if not using Google Maps
                   style={styles.map}
                   region={{
                       latitude: this.state.latitude,
                       longitude: this.state.longitude,
                     latitudeDelta: 0.09,
                     longitudeDelta: 0.035,
                   }}>
                  <Circle
                      center={{  latitude: this.state.latitude, longitude: this.state.longitude }}
                      radius = {3000}
                      fillColor={'rgba(200, 300, 200, 0.3)'}
                   />
                   {this.state.ready==true && (
                       <Marker
                              coordinate={{ latitude:this.state.latitude, longitude:this.state.longitude }}
                              title={'You Are Here'}>
                       </Marker>)
                   }
                   {this.state.dataSource.map(marker => (
                       <Marker
                          coordinate = {{ latitude: parseFloat(marker.latitude), longitude: parseFloat(marker.longitude) }}
                          title = {marker.title}
                          description = {marker.review}>
                       </Marker>
                   ))}
             </MapView>
        );
    }
}

const styles = StyleSheet.create({
     container: {
       ...StyleSheet.absoluteFillObject,
       height: 400,
       width: 400,
       justifyContent: 'flex-end',
       alignItems: 'center',
     },
     map: {
       height:'100%',
       ...StyleSheet.absoluteFillObject,
     },
});