import React from 'react';
import { FlatList, ActivityIndicator, Text, View, Image, TouchableHighlight  } from 'react-native';
import { GoogleSignin, GoogleSigninButton, statusCodes } from 'react-native-google-signin';
import {Platform} from 'react-native';

export default class ViewCategory extends React.Component<Props> {
	static navigationOptions = ({ navigation }) => {
		return {
		  title: "My subscription",
		};
	};

	constructor(props){
	  super(props);
	  this.state ={ isLoading: true};
      //this.web = 'http://explore-texas-web.appspot.com';
      this.web = 'http://apt-team7.appspot.com';
    //   this.web = 'https://explorexas.appspot.com';
	}

    async componentDidMount() {
        var that = this;
        var userInfo = await GoogleSignin.signInSilently();
        var userId = userInfo.user.email;
          const { navigation } = this.props;
          var url = that.web+'/mobile/list_subscribed_reports/'+userId
          console.log(url);

	  return fetch(url, {
	    method: "GET",
	    headers: {
    		'User-agent': 'android'
  		},
	  })
	  .then(function(res){
		console.log('request succeeded with JSON response', res)
	    res.json().then(function(data) {
	      console.log('request succeeded with JSON res//ponse', data)

	      that.setState({
	        isLoading: false,
	        dataSource: data,
	      }, function(){

	      });
	    }).catch(function(error) {
	      console.log('Data failed', error)
	    });
	}).catch(function(error){
	    console.log('request failed', error)
	})
	}


	_onPressButton(title, userId, userName, placeName, 
		categoryName, imgId, tag, review, rating, timeStamp, reportId) {
      console.log("View Report", title, userName, reportId);
      this.props.navigation.navigate('ViewRpt', {
				title: title,
				userId: userId,
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

	render()
	{
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
        <View style={{flex: 1, paddingTop:20, justifyContent:'center'}}>
          <FlatList
            data={this.state.dataSource}
            keyExtractor={(item, index) => item.imgId}
            renderItem={
              ({item}) => 
              <TouchableHighlight onPress={this._onPressButton.bind(this, item.title, item.userId, item.userName, item.placeName, item.categoryName, item.imgId, item.tag, item.review, item.rating, item.timeStamp, item.reportId)} underlayColor="white">
              <View style={{flex:1, flexDirection: 'row', height: 90, margin:5}} onPress={this._onPressButton.bind(this)}>
                <Image source={{uri: 'http://apt-team7.appspot.com/images/'+ item.imgId}} style={{flex:1}} />
                <View style={{flex:2.5, marginLeft:10}}>
                  <Text style={{color: 'blue', fontSize: 24}}>{item.title}</Text>
                  <Text style={{fontSize: 16}}>{item.userName}</Text>
                  <Text style={{fontSize: 16}}>{item.timeStamp}</Text>
                </View>
              </View>
              </TouchableHighlight>
            }
          />
        </View>
	);
	}
}
