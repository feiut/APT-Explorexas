import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import MapView, { PROVIDER_GOOGLE, Marker, Callout, Image, Circle } from 'react-native-maps'; // remove PROVIDER_GOOGLE import if not using Google Maps

export default class Map extends Component {
//     constructor(){
//        super();
//        this.state = {
//            ready: false,
//            where: {lat: null, lng: null},
//            error: null
//        }
//
//     }

//     componentDidMount(){
//        let geoOptions = {
//            enableHighAccuracy: true,
//            timeout: 20000,
//            maximumAge: 60 * 60 * 24
//        };
//        this.setState({ready: false});
//        geolocation.getCurrentPostion(this.geoSuccess,
//                                      this.geoFailure, geoOptions);
//     }
//        geoSuccess = (position) => {
//            this.setState({ready:true,
//                           where:{lat: position.coordinate.latitude,
//                           lng: position.coordinate.longitude}
//            })
//        }
//        geoFailure = (err) => {
//            this.setState({error: err.message});
//        }
     static navigationOptions =
     {
        title: 'View Reports on Map',
     };

    render(){
        return(
             <MapView
                   provider={PROVIDER_GOOGLE} // remove if not using Google Maps
                   style={styles.map}
                   region={{
                     latitude: 37.78825,
                     longitude: -122.4324,
//                     latitude: this.state.where.lat,
//                     longitude: this.state.where.lng,
                     latitudeDelta: 0.09,
                     longitudeDelta: 0.035,
                   }}>
                       <Circle
                           center={{  latitude: 37.7825259, longitude: -122.4353431 }}
                           radius = {3000}
                           fillColor={'rgba(200, 300, 200, 0.3)'}
                       />
                       <Marker
                           coordinate={{latitude: 37.7825259, longitude:-122.4353431}}
                           title={'San Francisco'}>
                       </Marker>

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