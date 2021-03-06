import React from 'react';
import { StyleSheet, Text, View, Button, Image, TouchableOpacity, ImageBackground} from 'react-native';
import { GoogleSignin, GoogleSigninButton, statusCodes } from 'react-native-google-signin';

export default class Home extends React.Component<Props> {
 static navigationOptions = (
 {
    title: 'Home',
 });

 openCategories() {
    console.log("View category");
    this.props.navigation.navigate('ViewAll');
  }

  createReport() {
    this.props.navigation.navigate('Create',{user : this.props.navigation.getParam('user')});
  }

  viewOnMap() {
    this.props.navigation.navigate('Map', {onlyNearby: false});
  }

  search() {
    this.props.navigation.navigate('Search');
  }

  personalInfo(){
    var img = this.props.navigation.getParam('img');
    if (img==null){
        img = "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg";
    }
    this.props.navigation.navigate('PersonInfo',{username: this.props.navigation.getParam('username'),
                                                 email: this.props.navigation.getParam('email'),
                                                 user: this.props.navigation.getParam('user'),
                                                 image: img});
  }

  subscription(){
    this.props.navigation.navigate('Subscription');
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
    var img = this.props.navigation.getParam('img');
    if (img == null){
        img = "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg";
    }
    console.log("img url", img);
    return(
       <View style = {styles.container}>
            <Text/>
            <Text/>
            <TouchableOpacity style={styles.imageContainer} onPress={this.personalInfo.bind(this)}>
                <Image source={{uri: img}} style={styles.image}/>
                <Image source={{uri: "https://theunstuckgroup.com/wp-content/uploads/2013/06/widget-personal-info.png"}} style={styles.smallImage}/>
            </TouchableOpacity>
            <Text/>
            <Text style={styles.title}> Hello! {this.props.navigation.getParam('username')} </Text>
            <Text/>
            <Text/>
            <Text/>
            <Button onPress={this.openCategories.bind(this)} title="ALL Categories"></Button>
            <Text></Text>
            <Button onPress={this.createReport.bind(this)} title="Create A New Report"></Button>
            <Text></Text>
            <Button onPress={this.viewOnMap.bind(this)} title="View Reports on Map"></Button>
            <Text></Text>
            <Button onPress={this.search.bind(this)} title="Search Tags"></Button>
            <Text></Text>
            <Button onPress={this.subscription.bind(this)} title="My subscription"></Button>
            <Text></Text>
            <Button onPress={this.signOut.bind(this)} title="Sign out"></Button>
       </View>
    );
 }
}
const styles = StyleSheet.create({
     container:{
       ...StyleSheet.absoluteFillObject,
       bottom: 0,
       justifyContent: 'flex-end',
     },
     imageContainer:{
        height: 130,
        width: 130,
        alignSelf:'center',
     },
     title: {
        color: 'black',
        fontSize: 20,
        alignSelf: 'center'
     },
     image: {
        width: 120,
        height: 120,
        alignSelf: 'center',
        borderRadius: 75,
        opacity: 0.9
     },
     smallImage: {
        width: 40,
        height: 40,
        position: 'absolute',
        bottom: 0,
        right: 0
     }
});

