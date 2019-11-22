import React,{ Component } from 'react';
import { Text, 
  View, 
  Picker, 
  TextInput, 
  StyleSheet, 
  SafeAreaView, 
  ScrollView,
  Image,
  TouchableOpacity,
  Alert, 
  PermissionsAndroid
} from 'react-native';
import Geolocation from 'react-native-geolocation-service';
import ImagePicker from 'react-native-image-picker';

export async function request_location_runtime_permission() {

  if(Platform.OS === 'ios'){
      try{
          const granted = await request(PERMISSIONS.IOS.LOCATION_WHEN_IN_USE);
          console.log('iPhone: '+ granted) ;
          if(granted === 'granted'){
               Alert.alert("Location Permission Granted.");
          }
      } catch(err){
          console.warn(err)
      }
  } else{
      try {
          const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            'title': 'ReactNativeCode Location Permission',
            'message': 'ReactNativeCode App needs access to your location '
          }
        )
        if (granted === PermissionsAndroid.RESULTS.GRANTED) {
          Alert.alert("Location Permission Granted.");
        }
        else {
          Alert.alert("Location Permission Not Granted");
        }
      } catch (err) {
        console.warn(err)
      }
  }
}

export default class CreateReport extends Component {
  static navigationOptions =
  {
     title: 'Create new report',
  };
  constructor(){
    super()
    this.state={
      image: null,
      title: '',
      placeName: '',
      category: '',
      review: '',
      tag: '',
      rating: '',
      image: '',
      latitude: '',
      longitude: '',
      photoloaded: false,
      photo: '',
      fileData: '',
      fileUri: ''
    }
    // this.url = 'https://explorexas.appspot.com/mobile_create_report'
    this.url = 'https://apt-team7.appspot.com/mobile_create_report'
  }
  
  async componentDidMount() {
    Geolocation.getCurrentPosition(position => {
      var myLatitude = position.coords.latitude;
      console.log("Current latitude", myLatitude);
      var myLongitude = position.coords.longitude;
      console.log("Current longitude", myLongitude);
      this.setState({ latitude: myLatitude,
                      longitude: myLongitude,
                      ready: true})
    },
    error => Alert.alert(error.message),
    { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
  )

}

  toHome = () =>{
    this.props.navigation.navigate('Home');
  }

  chooseImage = () => {
    let options = {
      title: 'Select Image',
      customButtons: [
        { name: 'customOptionKey', title: 'Choose Photo from Custom Option' },
      ],
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.showImagePicker(options, (response) => {
      // console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        const source = { uri: response.uri };
        // Also display the image using data:
        // const source = { uri: 'data:image/jpeg;base64,' + response.data };
        // alert(JSON.stringify(response));s
        console.log('response', JSON.stringify(response));
        this.setState({
          photoloaded:true,
          photo: response,
          fileData: response.data,
          fileUri: response.uri
        });
      }
    });
  }

  
  launchCamera = () => {
    let options = {
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.launchCamera(options, (response) => {
      // console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        // console.log('response', JSON.stringify(response));
        this.setState({
          photoloaded:true,
          photo: response,
          fileData: response.data,
          fileUri: response.uri
        });
      }
    });

  }

  launchImageLibrary = () => {
    let options = {
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.launchImageLibrary(options, (response) => {
      // console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        const source = { uri: response.uri };
        // console.log('response', JSON.stringify(response));
        this.setState({
          photoloaded:true,
          photo: response,
          fileData: response.data,
          fileUri: response.uri
        });
      }
    });

  }

  // renderFileData() {
  //   if (this.state.fileData) {
  //     return <Image source={{ uri: 'data:image/jpeg;base64,' + this.state.fileData }}
  //       style={styles.images}
  //     />
  //   } else {
  //     return <Image source={require('./assets/dummy.png')}
  //       style={styles.images}
  //     />
  //   }
  // }

  renderFileUri() {
    if (this.state.fileUri) {
      return <Image
        source={{ uri: this.state.fileUri }}
        style={styles.images}
      />
    } else {
      return <Image
        source={require('./assets/dummy.png')}
        style={styles.images}
      />
    }
  }

  handleUploadForm = () => {
    if(this.state.photoloaded == false){
      alert("Please Choose a Photo")
      return
    }
    if(this.state.category == ''){
      alert("Please Choose a Category")
      return
    }
    if(this.state.title == ''){
      alert("Please Enter a Title")
      return
    }
    const createFormData = (photo, body) => {
      const data = new FormData();
      data.append("file", {
        name: photo.fileName,
        type: photo.type,
        uri:
          Platform.OS === "android" ? photo.uri : photo.uri.replace("file://", "")
      });
    
      Object.keys(body).forEach(key => {
        data.append(key, body[key]);
      });
      console.log(data)
      return data;
    };

    // let photo = { uri: source.uri}
    let formdata = new FormData()
    // formdata.append("product[images_attributes[0][file]]", {uri: photo.uri, name: 'image.jpg', type: 'image/jpeg'})
    console.log("fileName",this.state.photo.fileName)
    console.log("type",this.state.photo.type)
    console.log("uri",this.state.photo.uri)
 
    fetch(this.url, {
      method: "POST",
	    headers: {
        'User-agent': 'android',
        'Content-Type': 'multipart/form-data'
			//'User-agent': Platform.OS
			},
      body: createFormData(
        this.state.photo,
        {
          "email": this.props.navigation.getParam("user").user.email,
          "title": this.state.title,
          "placeName": this.state.placeName,
          "categoryName": this.state.category,
          "review": this.state.review,
          "tagName": this.state.tag,
          "rating": this.state.rating,
          "latitude": this.state.latitude,
          "longitude": this.state.longitude
        }
      )
    })
      .then(response => response.json())
      .then(response => {
        console.log("upload succes", response);
        alert("Upload success!");
        this.setState({ photo: null });
      })
      .catch(error => {
        console.log("upload error", error);
        console.log(createFormData(
          this.state.photo,
          {
            "email": this.props.navigation.getParam("user").user.email,
            "title": this.state.title,
            "placeName": this.state.placeName,
            "categoryName": this.state.category,
            "review": this.state.review,
            "tagName": this.state.tag,
            "rating": this.state.rating,
            "latitude": this.state.latitude,
            "longitude": this.state.longitude
          }
        ))
        alert("Upload failed!");
      });
  };

 render()
 {
    return(
      <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.container_input}>
          <View style={styles.container_item}>
            <Text style={[styles.input_left]}>Titlel:</Text>
            <TextInput 
              style={styles.input_right} 
              placeholder="Title"
              onChangeText={(inputValue) => {
                this.setState({title: inputValue})
                console.log(this.state.title)}}></TextInput>    
          </View>
          <View style={styles.container_item}>
            <Text style={[styles.input_left]}>Place Name:</Text>
            <TextInput 
              style={styles.input_right} 
              placeholder="Place Name"
              onChangeText={(inputValue) => {
                this.setState({placeName: inputValue})}}></TextInput>    
          </View>
          <View style={styles.container_item}>
            <Text style={styles.input_left}>Category:</Text>
            <Picker style={styles.input_right} selectedValue={this.state.category}
              onValueChange={(itemValue) =>
                {this.setState({category: itemValue})
              console.log(this.state.category)}
                }>
              <Picker.Item label="Select Category" value="" />
              <Picker.Item label="Hiking" value="Hiking" />
              <Picker.Item label="Running" value="Running" />
              <Picker.Item label="Boating" value="Boating" />
              <Picker.Item label="Basketball" value="Basketball" />
              <Picker.Item label="Jogging" value="Jogging" />
              <Picker.Item label="Others" value="Others" />
            </Picker>
          </View>
          <View style={styles.container_item}>
            <Text style={[styles.input_left, styles.input_review]}>Review:</Text>
            <TextInput 
              multiline 
              style={[styles.input_right, styles.input_review]} 
              placeholder="Review"
              onChangeText={(inputValue) => {
                this.setState({review: inputValue})
                console.log(this.state.review)}}
            ></TextInput>
          </View>
          <View style={styles.container_item}>
            <Text style={[styles.input_left]}>Tag:</Text>
            <TextInput 
              style={styles.input_right} 
              placeholder="Tag"
              onChangeText={(inputValue) => {
                this.setState({tag: inputValue})
                console.log(this.state.tag)}}></TextInput>    
          </View>
          <View style={styles.container_item}>
            <Text style={styles.input_left}>Rating:</Text>
            <Picker style={styles.input_right} selectedValue={this.state.rating}
              onValueChange={(itemValue) =>
                this.setState({rating: itemValue})}>
              <Picker.Item label="Select Rating" value="" />
              <Picker.Item label="0" value="0" />
              <Picker.Item label="1" value="1" />
              <Picker.Item label="2" value="2" />
              <Picker.Item label="3" value="3" />
              <Picker.Item label="4" value="4" />
              <Picker.Item label="5" value="5" />
            </Picker>
          </View>

          <View style={styles.container_image}>
            <Text style={{textAlign:'left',paddingVertical:15}} >Choose Image:</Text>
            <View style={styles.ImageSections}>
              {/* <View>
                {this.renderFileData()}
              </View> */}
              <View>
                {this.renderFileUri()}
              </View>
            </View>

            <View style={styles.btnParentSection}>
              {/* <TouchableOpacity onPress={this.chooseImage} style={styles.btnSection}  >
                <Text style={styles.btnText}>Choose File</Text>
              </TouchableOpacity> */}

              <TouchableOpacity onPress={this.launchCamera} style={styles.btnSection}  >
                <Text style={styles.btnText}>Launch Camera</Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={this.launchImageLibrary} style={styles.btnSection}  >
                <Text style={styles.btnText}>Launch Gallery</Text>
              </TouchableOpacity>

          </View>
          </View>

        </View>
        <View style={styles.container_submit}>

          <TouchableOpacity onPress={this.handleUploadForm} style={styles.submit_btn}  >
            <Text style={styles.btnText}>Submit</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={this.toHome.bind(this)} style={[styles.submit_btn, styles.cancel_btn]}  >
            <Text style={styles.btnText}>Cancel</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
      </SafeAreaView>
    );
 }
}


const options = {
  title: 'Select Avatar',
  customButtons: [{ name: 'fb', title: 'Choose Photo from Facebook' }],
  storageOptions: {
    skipBackup: true,
    path: 'images',
  },
};

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    flexDirection: 'column',
    justifyContent: 'flex-start'
  },

  scrollView: {
    paddingHorizontal: 20,
    backgroundColor:'#ededed'
  },

  container_input:{
  },

  container_item:{
    flex: 1,
    flexDirection:'row',
    borderBottomWidth: .5
  },

  input_left: {
    flex: 1,
    flexDirection:'row',
    textAlignVertical:'center',
    height:50
  },

  input_right: {
    flex: 3,
    flexDirection:'row',
    height:50,
  },

  input_review:{
    height: 150,
    paddingTop: 8,
    textAlignVertical:'top'
  },

  container_image:{
    height: 300,
    borderBottomWidth: .5
  },

  container_submit:{
    paddingTop: 10,
    alignItems: 'center'
  },
  
  ImageSections: {
    display: 'flex',
    flexDirection: 'row',
    paddingHorizontal: 8,
    paddingVertical: 8,
    justifyContent: 'center'
  },
  images: {
    width: 250,
    height: 150,
    borderColor: 'black',
    borderWidth: 1,
    marginHorizontal: 3
  },
  btnParentSection: {
    alignItems: 'center',
    height: 100,
    flex:1,
    flexDirection: 'row',
    marginTop:10
  },
  btnSection: {
    width: 200,
    height: 50,
    flex: 1,
    backgroundColor: '#797D7F',
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 5,
    marginBottom:10
  },
  btnText: {
    textAlign: 'center',
    color: 'white',
    fontSize: 14,
    fontWeight:'bold'
  },
  submit_btn: {
    width: 280,
    height: 55,
    flex: 1,
    backgroundColor: '#5DADE2',
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 5,
    marginBottom:10
  },
  cancel_btn: {
    backgroundColor: '#979A9A'
  }
})