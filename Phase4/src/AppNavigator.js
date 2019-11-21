import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import Home from "./Home";
import Login from "./Login";
import ViewAllCategories from "./ViewAll";
import ViewCategory from "./ViewCat";
import Map from "./Map";
import SearchReport from "./SearchRpt"
import SearchResult from "./SearchRlt"
import ViewReports from"./ViewRpt"
import Template from "./Template";
import CreateReport from './CreateReport';

const AppNavigator = createStackNavigator({
    Login: Login,
    ViewAll: ViewAllCategories,
    ViewCat: ViewCategory,
    ViewRpt: ViewReports,
    Create: CreateReport,
    Map: Map,
    Search: SearchReport,
    SearchRlt: SearchResult,
    SignOut: Template,
    PersonInfo: PersonInfo,
    Home: Home
  }, {
    initialRouteName: "Login"
  });
  
  export default createAppContainer(AppNavigator);
