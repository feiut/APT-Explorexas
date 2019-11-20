import React from 'react';
import { StyleSheet, Text, View, Button} from 'react-native';
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
       <View style = {styles.container}>
            <Text style={styles.title}> Hello! {this.props.navigation.getParam('username')} </Text>
            <Text></Text>
            <Text></Text>
            <Text></Text>
            <Button onPress={this.openCategories.bind(this)} title="ALL Categories"></Button>
            <Text></Text>
            <Button onPress={this.createReport.bind(this)} title="Create A New Report"></Button>
            <Text></Text>
            <Button onPress={this.viewOnMap.bind(this)} title="View Reports on Map"></Button>
            <Text></Text>
            <Button onPress={this.search.bind(this)} title="Search Tags"></Button>
            <Text></Text>
            <Button onPress={this.signOut.bind(this)} title="Sign out"></Button>
       </View>
    );
 }
}
const styles = StyleSheet.create({
     container:{
       ...StyleSheet.absoluteFillObject,
       bottom:0,
       height: 400,
       justifyContent: 'flex-end',
     },
     title: {
        color: 'black',
        fontSize: 20,
        alignSelf: 'center'
     }
});

