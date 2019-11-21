import React from 'react';
import { Share, Text, View, Image, ScrollView, Platform, Button } from 'react-native';

export default class ViewReports extends React.Component<Props> {
 static navigationOptions =
 {
    title: 'View Report',
 };

 onShare = async() => {
    const { navigation } = this.props;
    var reportId = navigation.getParam('reportId','Others');
    const result = await Share.share({
        title: 'A Great Post Shared via Explorexas',
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
 }

 
 render()
 {
 	const { navigation } = this.props;
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
 	console.log(title, userName, categoryName, rating,reportId)

    return(
      <View style={{flex:1, flexDirection: 'column'}}>
        <Image source={{uri: 'http://explore-texas-web.appspot.com/images/'+ imgId}} style={{flex:2}} />
        <ScrollView>
        <View style={{flex:3, marginLeft:10}}>
          <Text style={{color: 'blue', fontSize: 24}}>{title}</Text>
          <Text style={{color: 'blue', fontSize: 16}}>{'#' + tag}</Text>
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
          <View>
            <Button onPress={this.onShare} title={'Share via Message'}> Share via Message</Button>
          </View>
        </View>
        </ScrollView>
      </View>
    );
 }
}
