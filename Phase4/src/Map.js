import React, { Component } from 'react';
import { StyleSheet, Text, View, Image, Platform, FlatList, Alert, PermissionsAndroid, Dimensions} from 'react-native';
import Geolocation from 'react-native-geolocation-service';
import MapView, { PROVIDER_GOOGLE, Marker, Callout, Circle } from 'react-native-maps'; // remove PROVIDER_GOOGLE import if not using Google Maps
import Carousel from 'react-native-snap-carousel';


export async function request_location_runtime_permission() {

  if(Platform.OS === 'ios'){
      try{
          const granted = await request(PERMISSIONS.IOS.LOCATION_WHEN_IN_USE);
          console.log('iPhone: '+ granted) ;
          if(granted === 'granted'){
               Alert.alert("Location Permission Granted.");
          }
      } catch(err){
          console.warn(err)
      }
  } else{
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
}

export default class Map extends Component {
     static navigationOptions =
     {
        title: 'View Reports on Map',
     };

     constructor(){
        super();
        this.state = {
            markers: [],
            latitude: 0,
            longitude: 0,
            ready : false,
            isLoading : true,
            dataSource : [],
            testData: [{"categoryName": "Test"},{"categoryName":"Another"}]
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
            'User-agent': 'android'
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

     _onMarkerPress(title, userName, placeName,
		categoryName, imgId, tag, review, rating, timeStamp) {
      console.log("View Report", title, userName);
      this.props.navigation.navigate('ViewRpt', {
      	title: title,
      	userName: userName,
      	placeName: placeName,
        categoryName: categoryName,
        imgId: imgId,
        tag: tag,
        review: review,
        rating: rating,
        timeStamp, timeStamp
      });
    }

    onCarouselItemChange = (index) => {
        let location = this.state.dataSource[index];

        this._map.animateToRegion({
            latitude: parseFloat(location.latitude),
            longitude: parseFloat(location.longitude),
            latitudeDelta: 0.09,
            longitudeDelta: 0.035
        })

        this.state.markers[index].showCallout()
    }

    renderCarouselItem = ({item, index}) => {
    return(
        <View style={styles.cardContainer}>
            <Text style={styles.cardTitle}> {item.title} </Text>
            <Text style={styles.cardText}> Category: {item.categoryName} </Text>
            <Text style={styles.cardText}> Place: {item.placeName} </Text>
            <Image style={styles.cardImage} source={{uri: 'http://apt-team7.appspot.com/images/'+ item.imgId}}/>
        </View>
    )
    }

    render(){
        return(
        <View style={styles.container}>
             <MapView
                   provider={PROVIDER_GOOGLE} // remove if not using Google Maps
                   style={styles.map}
                   ref={map => this._map=map}
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
                              coordinate={{ latitude:this.state.latitude, longitude:this.state.longitude }}>
                              <Callout>
                                <Text>You Are Here!</Text>
                              </Callout>
                       </Marker>)
                   }
                   {this.state.dataSource.map((marker, index) => (
                           <Marker
                              key={marker.reportId}
                              coordinate = {{ latitude: parseFloat(marker.latitude), longitude: parseFloat(marker.longitude) }}
                              title = {marker.title}
                              ref={ref => this.state.markers[index] = ref}>
                              <Callout onPress={() => {this._onMarkerPress(marker.title, marker.userName, marker.placeName,
                                                                  marker.categoryName, marker.imgId, marker.tag,
                                                                  marker.review, marker.rating, marker.timeStamp);}}>
                                  <Text>{marker.review}</Text>
                              </Callout>
                           </Marker>
                   ))}
             </MapView>
             <Carousel
                       ref={(c) => { this._carousel = c; }}
                       data={this.state.dataSource}
                       containerCustomStyle={styles.carousel}
                       renderItem={this.renderCarouselItem}
                       sliderWidth={Dimensions.get('window').width}
                       itemWidth={300}
                       onSnapToItem={(index)=> this.onCarouselItemChange(index)}
             />
        </View>
        );
    }
}

const styles = StyleSheet.create({
     container: {
       ...StyleSheet.absoluteFillObject,
//       height: 400,
       width: 450,
       justifyContent: 'flex-end',
       alignItems: 'center',
     },
     map:{
       height:'100%',
       ...StyleSheet.absoluteFillObject,
     },
     carousel: {
        position: 'absolute',
        bottom: 0,
        marginBottom: 48
     },
     cardContainer: {
        backgroundColor: 'rgba(0,0,0,0.8)',
        height: 220,
        width: 300,
        padding: 12,
        borderRadius: 22
     },
     cardTitle: {
        color: 'white',
        fontSize: 20,
        alignSelf: 'center'
     },
     cardText: {
        color: 'white',
        fontSize: 16,
        alignSelf: 'center'
     },
     cardImage: {
        height: 120,
        width: 300,
        bottom: 0,
        position: 'absolute',
        borderBottomLeftRadius: 22,
        borderBottomRightRadius: 22
     }
});