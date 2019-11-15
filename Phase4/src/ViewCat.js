import React from 'react';
import { Text, View  } from 'react-native';

export default class ViewCat extends React.Component<Props> {
 static navigationOptions =
 {
    title: 'Reports',
 };
 
 render()
 {
    const { params } = this.props.navigation.state;
    var catId = params.catId;
    console.log(catId);
    return(
       <View>
 
          <Text> Not implemented yet </Text>
 
       </View>
    );
 }
}