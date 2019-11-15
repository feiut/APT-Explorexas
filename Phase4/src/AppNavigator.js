import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import Home from "./Home";
import Login from "./Login";
import ViewAllCategories from "./ViewAll";
import ViewCategory from "./ViewCat";
import Template from "./Template";

const AppNavigator = createStackNavigator({
    Login: Login,
    ViewAll: ViewAllCategories,
    ViewCat: ViewCategory,
    Create: Template,
    Map: Template,
    Search: Template,
    SignOut: Template,
    Home: Home
  }, {
    initialRouteName: "Login"
  });
  
  export default createAppContainer(AppNavigator);