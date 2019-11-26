import React from 'react';
import { Text, View, StyleSheet, FlatList, Image, TouchableHighlight, Button  } from 'react-native';
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
    }

    onNotify(notify) {
      console.log(notify);
      this.props.navigation.navigate('Map');
      this.notif.scheduleNotify(10 ,"APT Notification Trial");
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
        console.log(this.state.enableNotify);
        return(
           <View style={styles.container}>
              <View style={styles.postsContainer}>
                  <Text style={styles.title}> Hello! {this.props.navigation.getParam('username')}</Text>
                  <Button onPress={this.scheduleNotification.bind(this)} title={enblNotify ? "Disable Notification" : "Enable Notification"}></Button>
                  <Text style={styles.secondTitle}> Your Posts: </Text>
                      <FlatList
                        data={this.state.dataSource}
                        keyExtractor={(item, index) => item.imgId}
                        renderItem={
                          ({item}) =>
                          <TouchableHighlight onPress={this._onPressButton.bind(this, item.title, item.userName, item.placeName, item.categoryName, item.imgId, item.tag, item.review, item.rating, item.timeStamp, item.reportId)} underlayColor="white">
                          <View style={{flex:1, flexDirection: 'row', height: 105, margin:5}} onPress={this._onPressButton.bind(this)}>
                            <Image source={{uri: 'http://apt-team7.appspot.com/images/'+ item.imgId}} style={{flex:1}} />
                            <View style={{flex:2.5, marginLeft:10}}>
                              <Text style={{color: 'blue', fontSize: 24}}>{item.title}</Text>
                              <Text style={{fontSize: 16}}>{item.placeName}</Text>
                              <Text style={{fontSize: 16}}>{item.timeStamp}</Text>
                              <Button title='Delete' onPress={this._onPressDelete(item.reportId)}/>
                            </View>
                          </View>
                          </TouchableHighlight>
                        }
                      />
              </View>
              <View style={styles.subscriptionsContainer}>
                <Text style={styles.secondTitle}> Your Subscription: </Text>
              </View>
           </View>
        );
     }
}

const styles = StyleSheet.create({
     container:{
       ...StyleSheet.absoluteFillObject,
       top: 0,
//       justifyContent: 'flex-end',
     },
     postsContainer:{
     },
     subscriptionsContainer: {
     },
     title: {
        color: 'black',
        fontSize: 30,
        alignSelf: 'center',
        backgroundColor: 'yellow'
     },
     secondTitle: {
        color: 'black',
        fontSize: 25,
     }
});
