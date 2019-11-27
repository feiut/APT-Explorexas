import React from 'react';
import { Share, Text, View, Image, ScrollView, Platform, Button, StyleSheet, Linking } from 'react-native';
import { GoogleSignin, GoogleSigninButton, statusCodes } from 'react-native-google-signin';
import { ActivityIndicator} from 'react-native';

export default class ViewReports extends React.Component<Props> {
 static navigationOptions =
 {
    title: 'View Report',
 };

  constructor(props){
    super(props);
    this.state ={isLoading: true, subscribed: false};
  }

  async componentDidMount() {
    var that = this;
    var userInfo = await GoogleSignin.signInSilently();
    var userId = userInfo.user.email;

    const url = 'https://arctic-sound-254923.appspot.com/mobile/get_subscriptions/' + userId;
    const author = this.props.navigation.getParam('userId', 'Others')
    console.log(url)
    return fetch(url, {
        method: "GET"
      })
      .then(function(res){
        res.json().then(function(data) {
            that.setState({
                isLoading: false,
                userId: userId,
                subscribed:  (data.some(item => author === item)),
              }, function(){
      
              });
        }).catch(function(error) {
          console.log('Data failed', error)
        });
    }).catch(function(error){
        console.log('request failed', error)
    })
  }

 onShare = async() => {
    const { navigation } = this.props;
    var reportId = navigation.getParam('reportId','Others');
    var placeName = navigation.getParam('placeName', 'Others');
 	var categoryName = navigation.getParam('categoryName', 'Others');
    const result = await Share.share({
        title: 'A Great Post About ' + categoryName +' in ' + placeName + ' Shared via Explorexas',
        message: 'This is a great post in Explorexas, and you should definitely check this out: https://apt-team7.appspot.com/reports/'+reportId,
    });
    console.log(result);
    if(result.action === Share.sharedAction){
        if(result.activityType){
            alert("Shared with "+result.activityType)
        }else{
            alert("Shared but not sure how")
        }
    }else if(result.action === Share.dismissedAction){
        alert("Share dismissed")
    }
 };

 onSubscribe() {
     var that = this;
     console.log("this.state=", this.state);
    var userId = this.state.userId;
    var operation = this.state.subscribed ? "unsubscribe" : "subscribe";
    var url = 'https://arctic-sound-254923.appspot.com/mobile/' + operation + '/' + userId + '/' + this.props.navigation.getParam('userId', 'Others')
    console.log(url);
    fetch(url, {
        method: "GET"
      })
      .then(function(res){
        that.state.subscribed = !that.state.subscribed;
        that.forceUpdate();
    }).catch(function(error){
        console.log('request failed', error)
    })
}
 onTagPress() {
    var tag = this.props.navigation.getParam('tag', 'Others');
    console.log('Search Report', tag)
	this.props.navigation.navigate('SearchRlt', {
	    keyWord: tag
	});
 }
// onLinkToWhatsapp = async() => {
//    const { navigation } = this.props;
//    var reportId = navigation.getParam('reportId','Others');
//    var text = 'This is a great post in Explorexas, and you should definitely check this out: https://apt-team7.appspot.com/reports/'+reportId;
//    Linking.openURL('whatsapp://send?text='+text);
// }

 render()
 {
     const { navigation } = this.props;
     var subscribed = this.state.subscribed;
     console.log("subscribed:", subscribed);
 	var title = navigation.getParam('title', 'Others');
 	var userName = navigation.getParam('userName', 'Others');
 	var placeName = navigation.getParam('placeName', 'Others');
 	var categoryName = navigation.getParam('categoryName', 'Others');
 	var imgId = navigation.getParam('imgId', 'Others');
 	var tag = navigation.getParam('tag', 'Others');
 	var review = navigation.getParam('review', 'Others');
 	var rating = navigation.getParam('rating', 'Others');
 	var timeStamp = navigation.getParam('timeStamp', 'Others');
 	var reportId = navigation.getParam('reportId','Others');
     console.log(title, userName, categoryName, rating, reportId);
     console.log(this.state.isLoading)
     if(this.state.isLoading){
        return(
          <View style={{flex:1, justifyContent:'center'}}>
            <View style={{flex: 1, padding: 20}}>
              <ActivityIndicator/>
            </View>
          </View>
        )
      }

    return(
      <View style={{flex:1, flexDirection: 'column'}}>
        <Image source={{uri: 'http://explore-texas-web.appspot.com/images/'+ imgId}} style={{flex:2}} />
        <ScrollView>
        <View style={{flex:3, marginLeft:10}}>
          <Text style={{color: 'blue', fontSize: 24}}>{title}</Text>
          <Text style={{color: 'blue', fontSize: 16}} onPress={this.onTagPress.bind(this)}>{'#' + tag}</Text>
          <View style ={{flexDirection: 'column'}}>
          	<Text style={{fontStyle:'italic', fontSize: 16, fontWeight: 'bold'}}>User</Text>
          	<Text style={{fontSize: 16}}>{userName}</Text>
          </View>
          <View style ={{flexDirection: 'column'}}>
          	<Text style={{fontStyle:'italic', fontSize: 16, fontWeight: 'bold'}}>Place</Text>
          	<Text style={{fontSize: 16}}>{placeName}</Text>
          </View>
          <View style ={{flexDirection: 'column'}}>
          	<Text style={{fontStyle:'italic', fontSize: 16, fontWeight: 'bold'}}>Review</Text>
          	<Text style={{fontSize: 16}}>{review}</Text>
          </View>
          <View style ={{flexDirection: 'column'}}>
          	<Text style={{fontStyle:'italic', fontSize: 16, fontWeight: 'bold'}}>Rating</Text>
          	<Text style={{fontSize: 16}}>{rating}</Text>
          </View>
          <View style ={{flexDirection: 'column'}}>
          	<Text style={{fontStyle:'italic', fontSize: 16, fontWeight: 'bold'}}>Category</Text>
          	<Text style={{fontSize: 16}}>{categoryName}</Text>
          </View>
          <View style ={{flexDirection: 'column'}}>
          	<Text style={{fontStyle:'italic', fontSize: 16, fontWeight: 'bold'}}>Time</Text>
          	<Text style={{fontSize: 16}}>{timeStamp}</Text>
          </View>
        </View>
        </ScrollView>
        <Button onPress={this.onShare} title={'Share This Post'} style={styles.shareButton}> Share This Post</Button>
        <Text></Text>
        <Button id="subscribe" onPress={this.onSubscribe.bind(this)} title={subscribed ? "Unsubscribe" : "Subscribe"} style={styles.shareButton}></Button>
      </View>
    );
 }
}
const styles = StyleSheet.create({
    shareButton: {
        position: 'absolute',
        bottom: 0,
        alignItems: 'center',
    }
});