import Foundation
import UIKit

class Settings {
    
    public static let HOST = "sravz.com" /// if url has "www" then add host like "www.domain.com" else would be white screen
    
    public static let URL = "https://sravz.com"
    public static let USER_AGENT:String = "Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36 Convertify"
    
    ///----------------------------- Local Html Setup Start ----------------------
    public static let OPEN_LOCAL_HTML_BY_DEFAULT = false
    public static let LOCAL_HTML_INDEX_PAGE = "Website/index.html" /// put your website data in folder "Website", index.html must be in Website main folder
    public static let OPEN_LOCAL_HTML_WHEN_OFFLINE = false
    ///----------------------------- Local Html Setup End ---------------------------
    
    public static let ALLOW_BACKWARD_FORWARD_GESTURE = true
    public static let ORIENTATION = 2 /// 0 for portrait, 1 for landscape, 2 for both
    
    public static let LOADING_SIGN = true
    public static let LOADING_SIGN_COLOR = HexColor.hexValue(hex: "#233714")
    
    public static let PULL_TO_REFRESH = true
    public static let RATE_DIALOG = true
    
    public static let STATUS_BAR_COLOR = HexColor.hexValue(hex: "#ffffff")
    public static let STATUS_BAR_TEXT_COLOR = 1  /// 0 for white, 1 for black
    
    public static let RATE_DIALOG_AFTER_APP_LAUNCHES = 3 /// dialog appears at 4th launch
    public static var PUSH_ENABLED = true
    
    public static let OPEN_SCAN_URL_IN_WEBVIEW = false
 
    ///----------------------------- External Links Setup Start --------------------------------------------------
    public static let EXTERNAL_LINKS_IN_BROWSER = false
    public static let WHITELIST_EXTERNAL_URLS = [
            "https://google.com",
            "https://www.facebook.com",
    ]
    ///----------------------------- External Links Setup End --------------------------------------------------
  
    ///----------------------------- Inject Setup Start --------------------------------------------------
    /// must put injection css and js files in CssJS folder
    public static let INJECT_CSS = false;
    public static let INJECT_CSS_FILENAME = "test"; ///  only name without extension
    public static let INJECT_JS = false;
    public static let INJECT_JS_FILENAME = "test"; /// only name without extension
    ///----------------------------- Inject Setup End ------------------------------------
    
    ///----------------------------- Inapp billing Setup Start --------------------------------------------------
    public static let IN_APP_PRODUCT_IDS = ["com.convertify.yourbundlename.PremiumProduct", "com.convertify.yourbundlename.PremiumProduct"]
    ///----------------------------- Inapp billing Setup Start --------------------------------------------------
    
    
    ///----------------------------- Drawer Setup Start --------------------------------------------------
    public static let SHOW_DRAWER = false
    // Note: Titles and icons arrays must have same number of values
    public static let DRAWER_TITLES = [
            "Home",
            "Notifications",
            "Account",
            "Home",
            "Notifications",
            "Account",
    ]
    public static let SHOW_DRAWER_ICONS = true
    public static let DRAWER_ICONS = [ // put the icons in Assests
            "testingIcon",
            "testingIcon",
            "testingIcon",
            "testingIcon",
            "testingIcon",
            "testingIcon",
    ]
    public static let DRAWER_LINKS = [
            "https://www.google.com",
            "https://www.facebook.com",
            "https://www.twitter.com"
    ]
    public static let TITLEBAR_TINT_COLOR = "white" /// color of icons and texts on titlebar (white or black)
    public static let TITLEBAR_BACKGROUND_COLOR = HexColor.hexValue(hex: "#000000")
    public static let DRAWER_BACKGROUND_COLOR = HexColor.hexValue(hex: "#dddddd")
    public static let DRAWER_ICON_COLOR = HexColor.hexValue(hex: "#000000")
    public static let DRAWER_TITLE_COLOR = HexColor.hexValue(hex: "#000000")
    ///----------------------------- Drawer Setup End --------------------------------------------------
    
    
    ///----------------------------- Bottom menu Setup Start --------------------------------------------------
    public static let SHOW_BOTTOM_MENU = false
    // Note: Bottom menu cannot have more than 5 items, Left Drawer can have more items
    // Note: Titles and icons arrays must have same number of values
    public static let BOTTOM_MENU_TITLES = [
            "Home",
            "Notifications",
            "Account",
    ]
    public static let SHOW_BOTTOM_MENU_ICONS = true
    public static let BOTTOM_MENU_ICONS = [ // put the icons in Assests
            "testingIcon",
            "testingIcon",
            "testingIcon",
    ]
    public static let BOTTOM_MENU_LINKS = [
            "https://www.google.com",
            "https://www.facebook.com",
            "https://www.twitter.com"
    ]
    public static let BOTTOM_MENU_SELECTED_ITEM_COLOR = HexColor.hexValue(hex: "#ffffff") /// color of selected item
    public static let BOTTOM_MENU_UNSELECTED_ITEM_COLOR = HexColor.hexValue(hex: "#ffffff") /// color of unselected item
    public static let BOTTOM_MENU_BACKGROUND_COLOR = HexColor.hexValue(hex: "#000000")
    ///----------------------------- Bottom menu Setup End --------------------------------------------------
    
    
    ///----------------------------- GIF Setup Start --------------------------------------------------
    // Put gif image file in "Gif" folder
    public static let SHOW_GIF_ANIMATION = false
    public static let GIF_LOAD_MAX_SECONDS: Double = 3
    public static let GIF_NAME = "animatedText" /// only name without extension
    ///----------------------------- GIF Setup End --------------------------------------------------
    
    ///----------------------------- Ads Setup Start --------------------------------------------------
    public static let ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"
    public static let ADMOB_BANNER_ID = "ca-app-pub-3940256099942544/6300978111"
    public static let ADMOB_INTERSTITIAL_ID = "ca-app-pub-3940256099942544/1033173712"
    public static let BANNER_AD = false
    public static let INTERSTITIAL_AD = false
    public static let INTERSTITIAL_AD_AFTER_CLICKS = 3 
    ///----------------------------- Ads Setup End --------------------------------------------------
    
}
