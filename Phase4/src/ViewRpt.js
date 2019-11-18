import React from 'react';
import { Text, View, Image, ScrollView } from 'react-native';

export default class ViewReports extends React.Component<Props> {
 static navigationOptions =
 {
    title: 'View Report',
 };

 
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
 	console.log(title, userName, categoryName, rating)

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
        </View>
        </ScrollView>
      </View>
    );
 }
}
