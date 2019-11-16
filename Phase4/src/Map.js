import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import MapView, { PROVIDER_GOOGLE, Marker, Callout, Image, Circle } from 'react-native-maps'; // remove PROVIDER_GOOGLE import if not using Google Maps

export default class Map extends Component {
     constructor(){
        super();
        this.state = {
            isLoading : true
//            ready: false,
//            where: {lat: null, lng: null},
//            error: null
        }

     }

     componentDidMount(){
      var that = this;
      return fetch('http://apt-team7.appspot.com/findReports', {
        method: "GET"
      })
      .then(function(res){
        res.json().then(function(data) {
          console.log('request succeeded with JSON response', data);
          that.setState({
            isLoading: false,
            dataSource: data,
          }, function(){

          });
        }).catch(function(error) {
          console.log('Map Data failed', error)
        });
    }).catch(function(error){
        console.log('Map request failed', error)
    })
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
     }

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
                     latitude: 30.2849,
                     longitude: -97.7341,
//                     latitude: this.state.where.lat,
//                     longitude: this.state.where.lng,
                     latitudeDelta: 0.09,
                     longitudeDelta: 0.035,
                   }}
                    data={this.state.dataSource}
                    keyExtractor={(item, index) => item.cat_id}
                    renderItem={
                      ({item}) =>
                          <Marker
                               coordinate={item.coordinates}
                               title= {item.title} >
                          </Marker>
                    }>
                       <Circle
                           center={{  latitude: 30.2849, longitude: -97.7341 }}
                           radius = {3000}
                           fillColor={'rgba(200, 300, 200, 0.3)'}
                       />
                       <Marker
                           coordinate={{latitude: 30.2849, longitude: -97.7341}}
                           title={'You Are Here'}>
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