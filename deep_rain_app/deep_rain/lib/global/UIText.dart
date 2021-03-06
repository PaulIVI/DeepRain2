import 'package:deep_rain/global/GlobalValues.dart';

/*
All text elements which are shown in the ui are stored here. Depending on the choosed language, other text will appear.
 */
class UIText{
  //ForecastList
  String forecastListAppTitle;
  String forecastListRainIntenseNoRain;
  String forecastListRainIntenseSomeRain;
  String forecastListRainIntenseMediumRain;
  String forecastListRainIntenseStrongRain;
  String forecastListRainIntenseError;

  //ForecastMap
  String forecastMapAppTitle;

  //Settings
  String settingsAppTitle;
  String settingsHeaderGeneral;
  String settingsLanguage;
  String settingsRegion;
  String settingsHeaderNotifications;
  String settingsRainWarning;
  String settingsTimeOfRainWarning;
  String settingsTimeOfRainWarningSubtitle;
    //Choose Language Dialog
    String chooseLanguageDialogHeader;
    String chooseLanguageDialogOkButton;
    //Choose Region Screen
    String chooseRegionScreenSearchHint;
    String chooseRegionScreenAwaitingForLocation;
    //Choose Time Screen
    String chooseWarningTimeScreen;
    String chooseWarningTimeDialogOkButton;
  String settingsHeaderMore;
  String settingsImpressum;
  String settingsDemoMode;

  //Impressum
  String impressumAppTitle;

  //Bottom Navigation
  String List;
  String Map;
  String Settings;


  UIText(){
    GlobalValues _globalValues = GlobalValues();
    if(_globalValues.getAppLanguage() == 'Deutsch'){
      //ForecastList
      forecastListAppTitle = 'Regenvorhersage';
      forecastListRainIntenseNoRain = 'Kein Regen';
      forecastListRainIntenseSomeRain = 'Leichter Regen';
      forecastListRainIntenseMediumRain = 'Mittlerer Regen';
      forecastListRainIntenseStrongRain = 'Starker Regen';
      forecastListRainIntenseError = 'Es gab einen Fehler';

      //ForecastMap
      forecastMapAppTitle = 'Regenkarte';

      //Settings
      settingsAppTitle = 'Einstellungen';
      settingsHeaderGeneral = 'Allgemeines';
      settingsLanguage = 'Sprache';
      settingsRegion = 'Region';
      settingsHeaderNotifications = 'Benachrichtigungen';
      settingsRainWarning = 'Regenwarnung';
      settingsTimeOfRainWarning = 'Zeitpunkt';
      settingsTimeOfRainWarningSubtitle = ' Minuten vor dem Regen';
        //choose language dialog
        chooseLanguageDialogHeader = 'Sprache auswählen';
        chooseLanguageDialogOkButton = 'Bestätigen';
        //Choose Region Screen
        chooseRegionScreenSearchHint = 'Stadt Suchen';
        chooseRegionScreenAwaitingForLocation = 'Am suchen...';
        //Choose Time Screen
        chooseWarningTimeScreen= "Zeitpunkt der Regenwarnung";
        chooseWarningTimeDialogOkButton= "Bestätigen";
      settingsHeaderMore = "Weiteres";
      settingsImpressum = "Impressum";
      settingsDemoMode = "Demo Modus";

      //Impressum
      impressumAppTitle = "Impressum";


      //Bottom Naviagation
      List = 'Liste';
      Map = 'Karte';
      Settings = 'Einstellungen';


    }
    else if(_globalValues.getAppLanguage() == 'Español'){
      //ForecastList
      forecastListAppTitle = 'Previsión de lluvia';
      forecastListRainIntenseNoRain = 'no llueve';
      forecastListRainIntenseSomeRain = 'Lluvia ligera';
      forecastListRainIntenseMediumRain = 'Lluvia media';
      forecastListRainIntenseStrongRain = 'Lluvia fuerte';
      forecastListRainIntenseError = 'Hubo un error';

      //ForecastMap
      forecastMapAppTitle = 'Mapa de la lluvia';

      //Settings
      settingsAppTitle = 'Ajustes';
      settingsHeaderGeneral = 'Información general';
      settingsLanguage = 'Idioma';
      settingsRegion = 'Región';
      settingsHeaderNotifications = 'Notificaciones';
      settingsRainWarning = 'Advertencia de lluvia';
      settingsTimeOfRainWarning = 'Fecha';
      settingsTimeOfRainWarningSubtitle = ' minutos antes de la lluvia';
        //choose language dialog
        chooseLanguageDialogHeader = 'Seleccione el idioma';
        chooseLanguageDialogOkButton = 'Confirme';
        //Choose Region Screen
        chooseRegionScreenSearchHint = 'Pesquisar';
        chooseRegionScreenAwaitingForLocation = 'Procurando por sua localização';
        //Choose Time Screen
        chooseWarningTimeScreen= "La hora de la advertencia de la lluvia";
        chooseWarningTimeDialogOkButton= "Confirme";
      settingsHeaderMore = "More";
      settingsImpressum = "Impressum";
      settingsDemoMode = "Modo demo";

      //Impressum
      impressumAppTitle = "Impressum";



      //Bottom Naviagation
      List = 'Lista';
      Map = 'Mapa';
      Settings = 'Ajustes';


    }
    else if(_globalValues.getAppLanguage() == 'English'){
      //ForecastList
      forecastListAppTitle = 'Rainforecast';
      forecastListRainIntenseNoRain = 'No rain';
      forecastListRainIntenseSomeRain = 'A little rain';
      forecastListRainIntenseMediumRain = 'Medium rain';
      forecastListRainIntenseStrongRain = 'Strong rain';
      forecastListRainIntenseError = 'There was an error';

      //ForecastMap
      forecastMapAppTitle = 'Rainfall map';

      //Settings
      settingsAppTitle = 'Settings';
      settingsHeaderGeneral = 'General';
      settingsLanguage = 'Language';
      settingsRegion = 'Region';
      settingsHeaderNotifications = 'Notifications';
      settingsRainWarning = 'Rainwarning';
      settingsTimeOfRainWarning = 'Warningtime';
      settingsTimeOfRainWarningSubtitle = ' minutes before the rain';
        //choose language dialog
        chooseLanguageDialogHeader = 'Choose Language';
        chooseLanguageDialogOkButton = 'Ok';
        //Choose Region Screen
        chooseRegionScreenSearchHint = 'Search City';
        chooseRegionScreenAwaitingForLocation = 'Searching...';
        //Choose Time Screen
        chooseWarningTimeScreen= "Time of rainwarning";
        chooseWarningTimeDialogOkButton= "Ok";
      settingsHeaderMore = "Otro";
      settingsImpressum = "Impressum";
      settingsDemoMode = "Demo Mode";

      //Impressum
      impressumAppTitle = "Impressum";

      //Bottom Naviagation
      List = 'List';
      Map = 'Map';
      Settings = 'Settings';
    }
  }
}

