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
  Modal,
  ActivityIndicator,
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

export default class CreateReport extends Component {
  static navigationOptions =
  {
     title: 'Create new report',
  };
  constructor(){
    super()
    this.state={
      isuploading: false,
      title: '',
      placeName: '',
      catList: ['Hiking', 'Running', 'Boating', 'Basketball', 'Jogging', 'Others'],
      category: '',
      review: '',
      tag: '',
      rating: '',
      image: '',
      latitude: '',
      longitude: '',
      photoloaded: false,
      showPopup: false,
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
  
  var that = this; 
  fetch('http://apt-team7.appspot.com/mobile', {
    method: "GET",
    userAgent: "android"
  })
  .then(function(res){
    res.json().then(function(data) {
      console.log('request succeeded with JSON response', data)
      var catList = data.map(cat => cat.catName);
      console.log('Caltlist', catList)
      that.setState({
        catList: catList,
      });
    }).catch(function(error) {
        console.log('Data failed', error)
      });
    }).catch(function(error){
        console.log('request failed', error)
    })

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
          // fileData: response.data,
          fileUri: response.uri
        });
      }
    });
  }

  
  launchCamera = () => {
    this.setState({showPopup: false});
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
          // fileData: response.data,
          fileUri: response.uri
        });
      }
    });

  }

  launchImageLibrary = () => {
    this.setState({showPopup: false});
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
          // fileData: response.data,
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
    if(this.state.rating == ''){
      alert("Please Enter a Rating")
      return
    }
    this.uploadForm()
  }
  
  uploadForm = () => {
    this.setState({ isuploading : true})
    console.log("fileName",this.state.photo.fileName)
    console.log("type",this.state.photo.type)
    console.log("uri",this.state.photo.uri)
    console.log("upload",this.state.isuploading)
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
        this.renderFileUri();
        this.setState({ 
          photo: null,
          isuploading : false,
          title: '',
          placeName: '',
          category: '',
          review: '',
          tag: '',
          rating: '',
          fileUri: '',
          photoloaded: false
         });
        console.log(this.state)
      })
      .catch(error => {
        this.setState({ isuploading : false });
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

 render(){
  let catItems = this.state.catList.map((cat, i) => {
    return <Picker.Item key={i} value={cat} label={cat} />
  });
  return(
    <SafeAreaView style={styles.container}>
    <Modal 
      animationType="fade"
      transparent={true}
      visible={this.state.showPopup}
      >
      <View style={{flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(0,0,0,0.5)'}}>
          
        <View style={styles.btnParentSection}>
          <TouchableOpacity onPress={this.launchCamera} style={[styles.btnSection,{borderBottomWidth: 0.5, borderBottomColor:'rgba(0,0,0,1)'}]}  >
            <Text style={styles.btnText}>Launch Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.launchImageLibrary} style={styles.btnSection}  >
            <Text style={styles.btnText}>Launch Gallery</Text>
          </TouchableOpacity>

        </View>
      </View>
    </Modal>
    <ScrollView style={styles.scrollView}>
      <View style={styles.container_input}>
        <View style={styles.container_item}>
          <Text style={[styles.input_left]}>Titlel:</Text>
          <TextInput 
            style={styles.input_right}
            // autoCorrect={false} 
            // ref={title => this.titleInput = title} 
            value={this.state.title} 
            placeholder="Title"
            onChangeText={(inputValue) => {
              this.setState({title: inputValue})
              console.log(this.state.title)}}></TextInput>    
        </View>
        <View style={styles.container_item}>
          <Text style={[styles.input_left]}>Place Name:</Text>
          <TextInput 
            value={this.state.placeName} 
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
            {catItems}
            {/* <Picker.Item label="Hiking" value="Hiking" />
            <Picker.Item label="Running" value="Running" />
            <Picker.Item label="Boating" value="Boating" />
            <Picker.Item label="Basketball" value="Basketball" />
            <Picker.Item label="Jogging" value="Jogging" />
            <Picker.Item label="Others" value="Others" /> */}
          </Picker>
        </View>
        <View style={styles.container_item}>
          <Text style={[styles.input_left, styles.input_review]}>Review:</Text>
          <TextInput 
            multiline 
            value={this.state.review} 
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
            value={this.state.tag} 
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
            <TouchableOpacity onPress={() => {this.setState({showPopup: true})}}>
              {this.renderFileUri()}
            </TouchableOpacity>
          </View>
        </View>

      </View>
      <View style={styles.container_submit}>

        <TouchableOpacity onPress={this.handleUploadForm} style={[styles.submit_btn]} disabled={this.state.isuploading} >
            { this.state.isuploading && <ActivityIndicator color='#ffffff' size='large'/> }
            { this.state.isuploading && <Text style={styles.submit_btnText}>Uploading</Text> }
            { !this.state.isuploading && <Text style={styles.submit_btnText}>Submit</Text> }
        </TouchableOpacity>

        <TouchableOpacity onPress={this.toHome.bind(this)} style={[styles.submit_btn, styles.cancel_btn]} disabled={this.state.isuploading} >
          <Text style={styles.submit_btnText}>Cancel</Text>
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
    height: 250,
    borderBottomWidth: .5
  },

  container_submit:{
    paddingBottom: 20,
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
    width: 280,
    height: 170,
    borderColor: 'black',
    borderWidth: 0.4,
    marginHorizontal: 3
  },
  btnParentSection: {
    alignItems: 'center',
    height: 100,
    flex: 0.2,
    flexDirection: 'column',
    marginTop: 10,
    backgroundColor: 'rgba(255,255,255,0.9)',
    borderRadius: 5
  },
  btnSection: {
    width: 280,
    height: 50,
    flex: 1,
    // backgroundColor: 'rgba(0,0,0,0.5)',
    alignItems: 'center',
    justifyContent: 'center'
  },
  btnText: {
    textAlign: 'center',
    color: 'black',
    fontSize: 18
  },
  submit_btnText: {
    textAlign: 'center',
    color: 'white',
    fontSize: 16
  },
  submit_btn: {
    width: 280,
    height: 55,
    flex: 1,
    flexDirection: 'row',
    backgroundColor: '#5DADE2',
    marginTop: 10,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 5
  },
  cancel_btn: {
    backgroundColor: '#979A9A'
  }
})