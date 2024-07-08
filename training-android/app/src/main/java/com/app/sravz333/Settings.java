package com.app.sravz333;

public class Settings {
    public static final String HOST = "sravz.com";//endparsehost
        public static final String HOME_URL = "https://sravz.com";//endparsehomeurl
    public static final String USER_AGENT = "Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36 Convertify";
    public static final int SCREEN_ORIENTATION = 0; // 0=BOTH, 1=PORTRAIT, 2=LANDSCAPE
    public static final boolean LOADING_SIGN = true;
    public static final String PLAY_STORE_LINK_ID = "com.app.sravz333"; // package name
    public static final boolean CACHE_ENABLED = true;
    public static boolean PUSH_ENABLED = true;
    public static final boolean OPEN_SCAN_URL_IN_WEBVIEW = false;

    //----------------------------- Inapp billing Setup Start --------------------------------------------------
    public static final String [] IN_APP_BILLING_PRODUCT_IDS = new String[] {};
    //----------------------------- Inapp billing Setup Start "product1","product2"--------------------------------------------------

    //----------------------------- External Links Setup Start --------------------------------------------------
    public static final boolean OPEN_EXTERNAL_LINKS_IN_BROWSER = false;
    public static final String [] WHITELIST_EXTERNAL_URLS = new String[]{
            "https://www.google.com",
            "https://www.facebook.com"
    };
    //----------------------------- External Links Setup End --------------------------------------------------


    //----------------------------- Pull to refresh Setup Start --------------------------------------------------
    public static final boolean PULL_TO_REFRESH = false;
    public static final int PULL_TO_REFRESH_POSITION_FROM_TOP = 50; // dp
    //----------------------------- Pull to refresh Setup End --------------------------------------------------


    //----------------------------- Splash Setup Start --------------------------------------------------
    // to remove splash you need to remove this line in AndroidManifest.xml file >> android:theme="@style/SplashTheme"
    public static final boolean SPLASH_SCREEN = true;
    public static final int SPLASH_SCREEN_TIMEOUT = 2000; // milliseconds
    //----------------------------- Splash Setup End --------------------------------------------------


    //----------------------------- Local Html Setup Start --------------------------------------------------
    public static final boolean OPEN_LOCAL_HTML_BY_DEFAULT = false;
    public static final String LOCAL_HTML_INDEX_PAGE = "index.html"; // filePath >> assets/website
    public static final boolean OPEN_LOCAL_HTML_WHEN_OFFLINE = false;
    //----------------------------- Local Html Setup End --------------------------------------------------


    //----------------------------- Inject Setup Start --------------------------------------------------
    public static final boolean INJECT_CSS = false;
    public static final String INJECT_CSS_FILENAME = "test.css"; // filePath >> assets/website/css (must create these folders if not exists)
    public static final boolean INJECT_JS = false;
    public static final String INJECT_JS_FILENAME = "test.js"; // filePath >> assets/website/js (must create these folders if not exists)
    //----------------------------- Inject Setup End --------------------------------------------------


    //----------------------------- Rate Dialog Setup Start --------------------------------------------------
    public static final boolean RATE_DIALOG = false;
    public static final int RATE_DIALOG_AFTER_APP_LANUCHES = 3;
    //----------------------------- Rate Dialog Setup End --------------------------------------------------


    //----------------------------- Ads Setup Start --------------------------------------------------
    public static final boolean BANNER_AD = false;
    public static final boolean INTERSTITIAL_AD = false;
    public static final int INTERSTITIAL_AD_AFTER_CLICKS = 5;
    //----------------------------- Ads Setup End --------------------------------------------------


    //----------------------------- Drawer Setup Start --------------------------------------------------
    public static final boolean SHOW_DRAWER = false;
    public static final String [] DRAWER_TITLES = new String[]{
            "Home",
            "Account",
            "Settings"
    };
    public static final boolean SHOW_DRAWER_ICONS = true;
    public static final int [] DRAWER_ICONS = new int[]{ // put the icons in res >  drawable folder
            R.drawable.home,
            R.drawable.account,
            R.drawable.settings
    };
    public static final String [] DRAWER_LINKS = new String[]{
            "https://www.google.com",
            "https://www.facebook.com",
            "https://www.twitter.com"
    };
    public static final String TITLEBAR_TINT_COLOR = "white"; // color of icons and texts on titlebar (white or black)
    public static final String TITLEBAR_BACKGROUND_COLOR = "#000000";
    public static final String DRAWER_BACKGROUND_COLOR = "#ffffff";
    public static final String DRAWER_ICON_COLOR = "#000000";
    public static final String DRAWER_TITLE_COLOR = "#000000";
    //----------------------------- Drawer Setup End --------------------------------------------------


    //----------------------------- Bottom menu Setup Start --------------------------------------------------
    public static final boolean SHOW_BOTTOM_MENU = false;
    // Note: Bottom menu cannot have more than 5 items, Left Drawer can have more items
    public static final String [] BOTTOM_MENU_TITLES = new String[]{
            "Home",
            "Account",
            "Settings"
    };
    public static final boolean SHOW_BOTTOM_MENU_ICONS = true;
    public static final int [] BOTTOM_MENU_ICONS = new int[]{ // put the icons in res >  drawable folder
            R.drawable.home,
            R.drawable.account,
            R.drawable.settings
    };
    public static final String [] BOTTOM_MENU_LINKS = new String[]{
            "https://www.google.com",
            "https://www.facebook.com",
            "https://www.twitter.com"
    };
    // Note: to change background, icon, text colors in bottom menu go to colors.xml file and edit bottomNavigationBackgroundColor, bottomNavigationActiveColor, bottomNavigationInActiveColor
    //----------------------------- Bottom menu Setup End --------------------------------------------------


    //----------------------------- GIF Setup Start --------------------------------------------------
    public static final boolean SHOW_GIF_ANIMATION = false;
    public static final int GIF_LOAD_MAX_SECONDS = 3;
    public static final int GIF_NAME = R.drawable.test1; // put the gif file in res > drawable folder
    //----------------------------- GIF Setup End --------------------------------------------------
}
