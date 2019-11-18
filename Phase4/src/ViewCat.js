import React from 'react';
import { FlatList, ActivityIndicator, Text, View, Image, TouchableHighlight  } from 'react-native';
import {Platform} from 'react-native';

export default class ViewCategory extends React.Component<Props> {
	static navigationOptions = ({ navigation }) => {
		return {
		  title: navigation.getParam('catName', 'Others'),
		};
	};

	constructor(props){
	  super(props);
	  this.state ={ isLoading: true};
      //this.web = 'http://explore-texas-web.appspot.com';
      this.web = 'http://apt-team7.appspot.com';
	}

	componentDidMount(){
		var that = this; 
  		const { navigation } = this.props;
		var cat_Id = navigation.getParam('catId', '5dab50f93763c3146ac201b9');
		var cat_Name = navigation.getParam('catName', 'Others');
		console.log(cat_Id, cat_Name);

	  return fetch(that.web+'/viewCategoryPost/'+cat_Id, {
	    method: "GET",
	    headers: {
    		'User-agent': Platform.OS
  		},
	  })
	  .then(function(res){
	    res.json().then(function(data) {
	      console.log('request succeeded with JSON response', data)

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


	_onPressButton(title, userName, placeName, 
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
              <TouchableHighlight onPress={this._onPressButton.bind(this, item.title, item.userName, item.placeName, item.categoryName, item.imgId, item.tag, item.review, item.rating, item.timeStamp)} underlayColor="white">
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