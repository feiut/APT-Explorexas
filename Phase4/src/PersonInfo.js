import React from 'react';
import { Text, View, StyleSheet, FlatList, Image, TouchableHighlight, Button, Alert  } from 'react-native';
import NotifyService from './NotifyService'

export default class PersonInfo extends React.Component<Props> {
     static navigationOptions =
     {
        title: 'Personal Info',
     };

     constructor(props){
          super(props);
          this.state = {
                isLoading: true,
                dataSource: [],
                enableNotify: false,
          };
          this.notif = new NotifyService(this.onNotify.bind(this));
     }

     buttonClicked = () => {
        Alert.alert(
          "Confirm",
          "Confirm to delete this report?",
          [
            { text: "Cancel", onPress: () => console.log("Cancel",reportId),
              style: "cancel"},
            {
              text: "Confirm", onPress: () => this._onPressDelete(reportId),
            }
          ],
          { cancelable: false }
        )
     }

    componentDidMount(){
      var that = this;
      var user_id = this.props.navigation.getParam('email');
      return fetch('http://apt-team7.appspot.com/mobileProfile/'+user_id, {
        method: "GET",
        userAgent: "android"
      }).then(function(res){
        res.json().then(function(data) {
          console.log('request succeeded with JSON response', data);
          that.setState({
            dataSource: data,
          });
        }).catch(function(error) {
          console.log('Report Data failed', error)
        });
    }).catch(function(error){
        console.log('request failed', error)
    })
    }

    _onPressButton(title, userName, placeName,
		categoryName, imgId, tag, review, rating, timeStamp, reportId) {
      console.log("View Report", title, userName, reportId);
      this.props.navigation.navigate('ViewRpt', {
      	title: title,
      	userName: userName,
      	placeName: placeName,
        categoryName: categoryName,
        imgId: imgId,
        tag: tag,
        review: review,
        rating: rating,
        timeStamp, timeStamp,
        reportId: reportId
      });
    }

    _onPressDelete(reportId) {
      console.log("Delete Report", reportId);
      fetch('http://apt-team7.appspot.com/deleteReport/'+reportId, {
        method: "GET",
        userAgent: "android"
      }).then(function(response){
        console.log(response)});
    }

    onNotify(notify) {
      console.log(notify);
      this.props.navigation.navigate('Map', {onlyNearby: true});
      this.notif.scheduleNotify(10 ,"Check out the nearby reports!");
    }

    scheduleNotification() {
      var enable = this.state.enableNotify;
      if(this.state.enableNotify) {
        this.notif.cancelAll();
      } else {
        this.notif.scheduleNotify(1 ,"APT Notification Trial");
      }
      this.setState({enableNotify: !enable});
    }

    cancelNotification() {
      this.notif.cancelAll();
    }

     render()
     {
        var enblNotify = this.state.enableNotify;
        var img = this.props.navigation.getParam('image');
        console.log("img url", img);
        return(
           <View style={styles.container}>
              <View style={styles.personCard}>
                 <Text style={styles.title}>{this.props.navigation.getParam('username')}</Text>
                 <Text style={styles.personalInfo}>Email: {this.props.navigation.getParam('email')}</Text>
                 <Image source={{uri: img}} style={styles.image}/>
              </View>
              <View style={styles.buttonView}>
                 <Button style={styles.buttonStyle} onPress={this.scheduleNotification.bind(this)} title={enblNotify ? "Disable Notification" : "Enable Notification"}></Button>
              </View>
              <Text style={styles.secondTitle}> Your Posts: </Text>
              <View style={styles.postsContainer}>
                      <FlatList
                        data={this.state.dataSource}
                        keyExtractor={(item, index) => item.imgId}
                        renderItem={
                          ({item}) =>
                          <TouchableHighlight onPress={this._onPressButton.bind(this, item.title, item.userName, item.placeName, item.categoryName, item.imgId, item.tag, item.review, item.rating, item.timeStamp, item.reportId)} underlayColor="white">
                          <View style={{flex:1, flexDirection: 'row', height: 110, margin:5}} onPress={this._onPressButton.bind(this)}>
                            <Image source={{uri: 'http://apt-team7.appspot.com/images/'+ item.imgId}} style={{flex:1}} />
                            <View style={{flex:2.5, marginLeft:10}}>
                              <Text style={{color: 'blue', fontSize: 24}}>{item.title}</Text>
                              <Text style={{fontSize: 16}}>{item.placeName}</Text>
                              <Text style={{fontSize: 16}}>{item.timeStamp}</Text>
                              <Button style={{height: 10}} title='Delete' onPress={()=>{ Alert.alert(
                                                                  "Confirm",
                                                                  "Confirm to delete this report?",
                                                                  [
                                                                    { text: "Cancel", onPress: () => console.log("Cancel",item.reportId),
                                                                      style: "cancel"},
                                                                    {
                                                                      text: "Confirm", onPress: () => this._onPressDelete(item.reportId),
                                                                    }
                                                                  ],
                                                                  { cancelable: false }
                                                                )}}/>
                            </View>
                          </View>
                          </TouchableHighlight>
                        }
                      />
              </View>
           </View>
        );
     }
}

const styles = StyleSheet.create({
     container:{
       ...StyleSheet.absoluteFillObject,
       top: 0,
     },
     personCard: {
       top: 0,
       height: 120,
       justifyContent: 'flex-end',
     },
     buttonView: {
       height: 45
     },
     postsContainer:{
     },
     image: {
        position:'absolute',
        top: 20,
        width: 80,
        height: 80,
        borderRadius: 75,
        marginLeft: 20
     },
     title: {
        position:'absolute',
        right: 20,
        top: 20,
        color: 'black',
        fontSize: 30,
        fontWeight: 'bold',
        alignSelf: 'center',
     },
     buttonStyle: {
        position:'absolute',
        top: 0
     },
     personalInfo: {
        position:'absolute',
        right: 20,
        top: 70,
        color: 'black',
        fontSize: 20,
        alignSelf: 'center',
     },
     secondTitle: {
        color: 'black',
        fontSize: 20,
        fontWeight: 'bold'
     }
});
