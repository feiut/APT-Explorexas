import React,{ Component } from 'react';
import { Text, 
  View, 
  Picker, 
  TextInput, 
  StyleSheet, 
  SafeAreaView, 
  ScrollView,
  Image,
  TouchableOpacity
} from 'react-native';
import ImagePicker from 'react-native-image-picker';

class FormItem extends Component{
  render(){
    return (
      <View style={styles.container_item}>
        <Text style={styles.input_left}>{this.props.name}:</Text>
        <TextInput multiline style={styles.input_right} placeholder={this.props.placeholder}></TextInput>
      </View>
    )
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
      geoLocation: '',
      filepath: {
        data: '',
        uri: ''
      },
      fileData: '',
      fileUri: ''
    }
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
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        const source = { uri: response.uri };

        // You can also display the image using data:
        // const source = { uri: 'data:image/jpeg;base64,' + response.data };
        // alert(JSON.stringify(response));s
        console.log('response', JSON.stringify(response));
        this.setState({
          filePath: response,
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
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        const source = { uri: response.uri };
        console.log('response', JSON.stringify(response));
        this.setState({
          filePath: response,
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
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        const source = { uri: response.uri };
        console.log('response', JSON.stringify(response));
        this.setState({
          filePath: response,
          fileData: response.data,
          fileUri: response.uri
        });
      }
    });

  }

  renderFileData() {
    if (this.state.fileData) {
      return <Image source={{ uri: 'data:image/jpeg;base64,' + this.state.fileData }}
        style={styles.images}
      />
    } else {
      return <Image source={require('./assets/dummy.png')}
        style={styles.images}
      />
    }
  }

  // renderFileUri() {
  //   if (this.state.fileUri) {
  //     return <Image
  //       source={{ uri: this.state.fileUri }}
  //       style={styles.images}
  //     />
  //   } else {
  //     return <Image
  //       source={require('./assets/galeryImages.jpg')}
  //       style={styles.images}
  //     />
  //   }
  // }



 render()
 {
    return(
      <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.container_input}>
          <FormItem name="Title" placeholder="Title"/>
          <FormItem name="Place Name" placeholder="Place Name"/>
          <View style={styles.container_item}>
            <Text style={styles.input_left}>Category:</Text>
            <Picker style={styles.input_right} selectedValue={this.state.category}
              onValueChange={(itemValue) =>
                this.setState({category: itemValue})}>
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
            <TextInput multiline style={[styles.input_right, styles.input_review]} placeholder="Review"></TextInput>
          </View>
          <FormItem name="Tag" placeholder="Tag"/>
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
              <View>
                {this.renderFileData()}
                {/* <Text  style={{textAlign:'center'}}>Base 64 String</Text> */}
              </View>
              {/* <View>
                {this.renderFileUri()}
                <Text style={{textAlign:'center'}}>File Uri</Text>
              </View> */}
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

          <TouchableOpacity onPress={this.toHome.bind(this)} style={styles.submit_btn}  >
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