import React from 'react';
import { FlatList, ActivityIndicator, Text, View, Image, TouchableHighlight  } from 'react-native';
import { SearchBar } from 'react-native-elements';

export default class SearchReport extends React.Component<Props> {
	 static navigationOptions =
	 {
	    title: 'Search',
	 };

	constructor(props){
	  super(props);
	  this.state ={ search:""};
	}

  	updateSearch (text) {
    	this.setState({ search:text });
  	};

	performSearch() {
	  console.log("Perform Search", this.state.search);
	  this.props.navigation.navigate('SearchRlt', {
	    keyWord: this.state.search
	  });
	}

	render()
	{
		return(
			<View style={{flex: 1, paddingTop:20, justifyContent:'flex-start'}}>
			  <SearchBar
	          round
	          lightTheme
	          platform="android"
	          icon={{ type: 'font-awesome', name: 'search' }}
	          inputStyle={{backgroundColor: 'white'}}
	          containerStyle={{backgroundColor: 'white', borderWidth: 1, borderRadius: 5}}	
	          searchIcon={{ size: 24 }}
	          onSubmitEditing={()=>this.performSearch()}
	          onChangeText={(text)=>this.updateSearch(text)}
	          placeholder="Search Tag Here"
	          value={this.state.search}
	      />
	     </View>
		)      			
	 }	
}