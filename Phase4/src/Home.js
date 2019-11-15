import React from 'react';
import { Text, View, Button} from 'react-native';
import { GoogleSignin, GoogleSigninButton, statusCodes } from 'react-native-google-signin';

export default class Home extends React.Component<Props> {
 static navigationOptions =
 {
    title: 'Home',
 };

 openCategories() {
    console.log("View category");
    this.props.navigation.navigate('ViewAll');
  }

  createReport() {
    this.props.navigation.navigate('Create');
  }

  viewOnMap() {
    this.props.navigation.navigate('Map');
  }

  search() {
    this.props.navigation.navigate('Search');
  }

  signOut = async () => {
    try {
      await GoogleSignin.revokeAccess();
      await GoogleSignin.signOut();
      this.setState({ user: null, loggedIn: false });
    } catch (error) {
      console.warn(error);
    }

    this.props.navigation.navigate('Login');
  };

 render()
 {
    

    return(
       <View>
 
            <Button onPress={this.openCategories.bind(this)} title="Categories"></Button>
            <Text></Text>
            <Button onPress={this.createReport.bind(this)} title="Create Report"></Button>
            <Text></Text>
            <Button onPress={this.viewOnMap.bind(this)} title="View on Map"></Button>
            <Text></Text>
            <Button onPress={this.search.bind(this)} title="Search"></Button>
            <Text></Text>
            <Button onPress={this.signOut.bind(this)} title="Sign out"></Button>
 
       </View>
    );
 }
}