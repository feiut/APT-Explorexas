// Login.js
import React from 'react'
import { StyleSheet, Text, TextInput, View, Button } from 'react-native'
import firebaseConfig from './firebaseConfig';
import { GoogleSignin, GoogleSigninButton, statusCodes } from 'react-native-google-signin';
import withFirebaseAuth from 'react-with-firebase-auth'
import * as firebase from 'firebase/app';
import 'firebase/auth';

export default class Login extends React.Component {
  state = { isSigninInProgress: false, errorMessage:null };

  static navigationOptions =
  {
      title: 'Login',
  };

  _signIn = async () => {
    // Todo: 
    // Currently login won't succeed (it returns a DEVELOPER_ERROR)
    // I believe this is because the firebase config file (/android/app/google-services.json) is incorrect. 
    // I copied the firebase config file from phase 3, but we are supposed to have a different config file
    // Please get a new cofiguration file for this project, and I think then the login should work

    try {
      await GoogleSignin.configure();
      const userInfo = await GoogleSignin.signIn();
      this.setState({ userInfo: userInfo, loggedIn: true });
      console.log(userInfo);
      this.props.navigation.navigate('Home', {
        user: userInfo
      });
    } catch (error) {
      if (error.code === statusCodes.SIGN_IN_CANCELLED) {
        // user cancelled the login flow
      } else if (error.code === statusCodes.IN_PROGRESS) {
        // operation (f.e. sign in) is in progress already
      } else if (error.code === statusCodes.PLAY_SERVICES_NOT_AVAILABLE) {
        // play services not available or outdated
      } else {
        // some other error happened
        console.warn(error.code);
        // Todo: comment this after fixing the login issue! Should only redirect to Home after a successful login
        this.props.navigation.navigate('Home');
      }
    }
  };

  render() {
    return (
      <View>
         
        <GoogleSigninButton
          style={{ width: 192, height: 48 }}
          size={GoogleSigninButton.Size.Wide}
          color={GoogleSigninButton.Color.Dark}
          onPress={this._signIn}
          disabled={this.state.isSigninInProgress} />

        {this.state.errorMessage &&
          <Text style={{ color: 'red' }}>
            {this.state.errorMessage}
          </Text>}
      </View>
    )
  }
}