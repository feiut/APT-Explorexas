import React from 'react';
import { FlatList, ActivityIndicator, Text, View, Image, TouchableHighlight  } from 'react-native';

export default class ViewAllCategories extends React.Component<Props> {

    static navigationOptions =
    {
        title: 'Categories',
    };
    
    constructor(props){
      super(props);
      this.state ={ isLoading: true}
    }
  
    componentDidMount(){
      var that = this; 
  
      return fetch('http://apt-team7.appspot.com/mobile', {
        method: "GET",
        userAgent: "android"
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
  
    _onPressButton(cat_id) {
      console.log("View category", cat_id);
      this.props.navigation.navigate('ViewCat', {
        catId: cat_id
      });
    }
  
    render(){
  
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
            keyExtractor={(item, index) => item.cat_id}
            renderItem={
              ({item}) => 
              <TouchableHighlight onPress={this._onPressButton.bind(this, item.cat_id)} underlayColor="white">
              <View style={{flex:1, flexDirection: 'row', height: 90, margin:5}} onPress={this._onPressButton.bind(this)}>
                <Image source={{uri: "https://arctic-sound-254923.appspot.com/images/" + item.imageId}} style={{flex:1}} />
                <View style={{flex:2.5, marginLeft:10}}>
                  <Text style={{color: 'blue', fontSize: 24}}>{item.catName}</Text>
                  <Text style={{fontSize: 16}}>{item.catDescription}</Text>
                </View>
              </View>
              </TouchableHighlight>
            }
          />
        </View>
      );
    }
  }