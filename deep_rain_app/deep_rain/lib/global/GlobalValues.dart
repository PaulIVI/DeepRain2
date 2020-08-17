import 'dart:convert';

import 'package:deep_rain/services/FindPixel.dart';
import 'package:flutter/services.dart';
import 'package:latlong/latlong.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:ml_linalg/linalg.dart';
import 'dart:math';

/*
All variables which need to be accesed are stored here. If a variable changes, the set method will be called.
The new value will be stored on the global variable which starts with "App...". It also will be stored in SharedPreferences (Local Key Value DB).
On Appstart the global values will be set from the data which is stored in shared preferences.
 */

//time of push notification
Duration AppTimeBeforeWarning;
// uid of the devide
String AppDeviceToken;
// to delete the old one if time of push notification changes
String AppLastDeviceTokenDocument;
// to delete the token in the older collection
String AppLastRegionDocument;
// push notification or not
bool AppSwitchRainWarning;
// the language
String AppLanguage;
// the region in which the app is used (latitude and longitude)
LatLng AppRegion;
// the name of the City, for UI.
String AppRegionCity;
// Lists which are needed to calculate the pixel in the forecast image
List<String> AppCoordinateList;
List<String> AppLatitudeList;
List<String> AppLongitudeList;
var AppPixel;

class GlobalValues{

  //How long before the rain the user want to get his push notification
  setTimeBeforeWarning(Duration TimeBeforeWarning) async{
    AppTimeBeforeWarning = TimeBeforeWarning;
    final prefs = await SharedPreferences.getInstance();
    prefs.setInt('AppTimeBeforeWarning', TimeBeforeWarning.inMinutes);
  }
  Duration getTimeBeforeWarning(){
    return AppTimeBeforeWarning;
  }

  //A uniq devicetoken wich also is stored in the firestorage. It is needed from cloud functions to send push notification.
  setDeviceToken(String DeviceToken) async{
    AppDeviceToken = DeviceToken;
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppDeviceToken', DeviceToken);
  }
  String getDeviceToken(){
    return AppDeviceToken;
  }

  //If the time of rain warning changes, the old devicetoken need to be deleted and stored in a other collection.
  //The document which need to be replaced is stored here.
  setAppLastDeviceTokenDocument(String LastDeviceTokenDocument) async{
    AppLastDeviceTokenDocument = LastDeviceTokenDocument;
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppLastDeviceTokenDocument', LastDeviceTokenDocument);
  }
  String getAppLastDeviceTokenDocument(){
    return AppLastDeviceTokenDocument;
  }

  //If the region changes, the old region need to be deleted and stored in a other collection.
  //The document which need to be replaced is stored here.
  setAppLastRegionDocument(String LastRegionDocument) async{
    AppLastRegionDocument = LastRegionDocument;
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppLastRegionDocument', LastRegionDocument);
  }
  String getAppLastRegionDocument(){
    return AppLastRegionDocument;
  }

  //Variable which store if push notification is activated or deactivated
  setAppSwitchRainWarning(bool SwitchRainWarning) async{
    AppSwitchRainWarning = SwitchRainWarning;
    final prefs = await SharedPreferences.getInstance();
    prefs.setBool('AppSwitchRainWarning', AppSwitchRainWarning);

  }
  getAppSwitchRainWarning(){
    if(AppSwitchRainWarning != null){
      return AppSwitchRainWarning;
    }
    return true;
  }

  //The UI language of the app.
  setAppLanguage(String Language) async {
    AppLanguage = Language;
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppLanguage', AppLanguage);
  }
  String getAppLanguage(){
    if(AppLanguage != null){
      return AppLanguage;
    }
    return "Deutsch";
  }

  //The region of the app.
  setAppRegion(LatLng Region) async {
    AppRegion = Region;
    final prefs = await SharedPreferences.getInstance();
    prefs.setDouble('AppRegionLatitude', AppRegion.latitude);
    prefs.setDouble('AppRegionLongitude', AppRegion.longitude);
  }
  LatLng getAppRegion(){
    if(AppRegion != null){
      return AppRegion;
    }
    return LatLng(47.666947, 9.170982);
  }

  //The name of the city which the user choosed
  setAppRegionCity(String City) async {
    AppRegionCity = City;
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppRegionCity', AppRegionCity);
  }
  String getAppRegionCity(){
    if(AppRegionCity != null){
      return AppRegionCity;
    }
    return "Konstanz";
  }

  //Store the coordinate List
  setCoordinateLists(String CoordinateList) async{
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppCoordinateList', CoordinateList);
  }
  List<dynamic> getCoordinateLists(){
    return AppCoordinateList;
  }
  //Store the latitude List
  setLatitudeList(String LatitudeList) async{
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppLatitudeList', LatitudeList);
  }
  List<dynamic> getLatitudeList(){
    return AppLatitudeList;
  }
  //Store the longitude List
  setLongitudeList(String LongitudeList) async{
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('AppLongitudeList', LongitudeList);
  }
  List<dynamic> getLongitudeList(){
    return AppLongitudeList;
  }

  // convert json file to String
  Future<String> loadListCoordinates() async {
    final ByteData data = await rootBundle.load('assets/data/listCoordinates.json');
    String jsonContent = utf8.decode(data.buffer.asUint8List());
    return jsonContent;
  }

  // convert json file to String
  Future<String> loadListLatitude() async {
    final ByteData data = await rootBundle.load('assets/data/listLatitudeComplete.json');
    String jsonContent = utf8.decode(data.buffer.asUint8List());
    return jsonContent;
  }

  // convert json file to String
  Future<String> loadListLongitude() async {
    final ByteData data = await rootBundle.load('assets/data/listLongitudeComplete.json');
    String jsonContent = utf8.decode(data.buffer.asUint8List());
    return jsonContent;
  }

  // store the pixel of the region in the forecast image (as x and y)
  setAppPixel(var Pixel) async{
    AppPixel = Pixel;
    final prefs = await SharedPreferences.getInstance();
    prefs.setInt('AppPixel_X', Pixel[0]);
    prefs.setInt('AppPixel_Y', Pixel[1]);
  }

  getAppPixel() async{
    print('APPPIXEL');
    print(AppPixel);
    // use the already calculated pixel
    if(AppPixel != null){
      return AppPixel;
    }
    // calculate the pixel
    if(AppPixel == null){
      changeAppPixel();
    }
  }

  // calculate the coordinates of the new pixel, based on AppRegion
  changeAppPixel() async{
    print('Ich berechne jetzt den Pixel!');
    // get the string with all items of the list
    String coordinateListString = await loadListCoordinates();
    String latitudeListString = await loadListLatitude();
    String longitudeListString = await loadListLongitude();

    // get the lists from the Strings
    var coordinateListVar = await json.decode(coordinateListString);
    var longitudeListVar = await jsonDecode(longitudeListString);
    var latitudeListVar = await jsonDecode(latitudeListString);

    print('TADAAA');
    print(coordinateListVar[100]);
    print(longitudeListVar[100]);
    print(latitudeListVar[100]);

    double latitude = AppRegion.latitude;
    double longitude = AppRegion.longitude;
    print(latitude);
    print(longitude);

    // here the right pixel should be calculated, not working yez, so always set [300,200]
    //FindPixel hey = FindPixel();
//    var longitude_min = longitudeListVar.reduce((curr, next) => curr < next? curr: next);
//    var longitude_max = longitudeListVar.reduce((curr, next) => curr > next? curr: next);
//    var latitude_min = latitudeListVar.reduce((curr, next) => curr < next? curr: next);
//    var latitude_max = latitudeListVar.reduce((curr, next) => curr > next? curr: next);
    //var pixels = hey.getClosest_Coordinate(longitudeListVar, latitudeListVar, 899, 0, 899, 0, AppRegion.longitude, AppRegion.latitude);

    var pixels = [300,200];

    print('The new Coordinates of the Pixel are: ');
    print(pixels);

    coordinateListVar = null;
    longitudeListVar = null;
    latitudeListVar  = null;

    await setAppPixel(pixels);

    print('Ich berechne jetzt den Pixel! 5');

    return pixels;
  }

}
