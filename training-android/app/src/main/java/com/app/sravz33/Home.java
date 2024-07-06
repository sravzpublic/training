package com.app.sravz33;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;
import android.Manifest;
import android.app.Activity;
import android.app.DownloadManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Message;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewTreeObserver;
import android.webkit.CookieManager;
import android.webkit.CookieSyncManager;
import android.webkit.DownloadListener;
import android.webkit.GeolocationPermissions;
import android.webkit.PermissionRequest;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebStorage;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.Toast;
import com.app.sravz33.util.AdUtil;
import com.app.sravz33.util.BottomMenuUtil;
import com.app.sravz33.util.DrawerUtil;
import com.app.sravz33.util.FilePicker;
import com.app.sravz33.util.GifUtil;
import com.app.sravz33.util.InAppBilling;
import com.app.sravz33.util.InjectUtil;
import com.app.sravz33.util.IntentUtil;
import com.app.sravz33.util.LinkUtil;
import com.app.sravz33.util.LogUtil;
import com.app.sravz33.util.MyJavaScriptInterface;
import com.app.sravz33.util.NetworkUtil;
import com.app.sravz33.util.PermissionUtil;
import com.app.sravz33.util.PrefsUtil;
import com.app.sravz33.util.RateDialogUtil;
import com.app.sravz33.util.SplashUtil;
import com.app.sravz33.util.TimerUtil;
import com.app.sravz33.util.Utils;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.onesignal.OSPermissionSubscriptionState;
import com.onesignal.OneSignal;

public class Home extends AppCompatActivity {
    SwipeRefreshLayout pullToRefresh; // parent view
    WebView webView;
    ViewGroup noInternet;
    ViewGroup adParent;
    String mGeoLocationRequestOrigin = null;
    GeolocationPermissions.Callback mGeoLocationCallback = null;
    PermissionRequest permissionRequest;
    public ValueCallback<Uri> mUploadMessage;
    public ValueCallback<Uri[]> mFilePathCallback;
    String userId = "";
    boolean showingLocalWebsite = false;
    ViewGroup container;
    ViewGroup gifAnim;
    ImageView gifAnimImg;
    private WebView mWebviewPop;
    private String target_url_prefix = Settings.HOST;
    TimerUtil timerUtil;
    DrawerUtil drawerUtil;
    InAppBilling inAppBilling;

    public static String currentUrl = Settings.HOME_URL;
    public static boolean showRateDialog;
    public static int linkClicks = 0;
    public static boolean homeLoaded = false;
    public static Uri mPhotoCapturedURI;
    public static final int LOC_PERMISSION = 100;
    public static final int VIDEO_CAPTURE_PERMISSION1 = 1001;
    public static final int VIDEO_CAPTURE_PERMISSION2 = 1002;
    public static final int DOWNLOAD_PERMISSION = 102;
    public static final int READ_PERMISSION = 103;
    public static final int WRITE_PERMISSION = 104;
    public static final int CAMERA_PERMISSION = 105;
    public static final int AUDIO_PERMISSION = 106;
    public final static int FILECHOOSER_RESULTCODE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Utils.setScreenOrientation(this);
        if(!Settings.SHOW_DRAWER && !Settings.SHOW_BOTTOM_MENU){
            setContentView(R.layout.activity_home);
            init();
        }
        else{
            setContentView(R.layout.activity_home_drawer);
            init();
        }

        if(Settings.SHOW_DRAWER){
            drawerUtil = new DrawerUtil(this);
            drawerUtil.setupDrawer();
        }
        if(Settings.SHOW_BOTTOM_MENU){
            BottomMenuUtil.setBottomMenu(this);
        }

        if(Settings.SHOW_GIF_ANIMATION){
            GifUtil.showGifAnimation(this, gifAnim, gifAnimImg);
        }
        else{
            GifUtil.hideGifAnimation(gifAnim);
        }

        Settings.PUSH_ENABLED = PrefsUtil.isPushEnabled(this);

        setInitialUrl();
        LogUtil.loge("url: "+currentUrl);

        setStatusBarColor();
        setPulltoRefresh();
        setupWebView(webView, false);
        loadWebPage();
        if(Settings.SPLASH_SCREEN) {
            SplashUtil.showSplash(this);
        }

        PrefsUtil.setAppLanuches(this, PrefsUtil.getAppLanuches(this)+1);

        if(Settings.RATE_DIALOG) {
            showRateDialog = RateDialogUtil.shouldShow(this);
        }

        AdUtil.loadBannerAd(this, adParent);

        inAppBilling = new InAppBilling();
        inAppBilling.setupBillingClient(this);
        // check latest url in webview every second
        timerUtil = new TimerUtil();
        timerUtil.startTimer(webView);

        registerReceiver(CloseHome, new IntentFilter("close"));
    }

    private void init() {
        container = findViewById(R.id.container);
        webView = findViewById(R.id.webView);
        pullToRefresh = findViewById(R.id.pullToRefresh);
        adParent = findViewById(R.id.adParent);
        noInternet = findViewById(R.id.noInternet);
        gifAnim = findViewById(R.id.gifAnim);
        gifAnimImg = findViewById(R.id.gifAnimImg);
    }

    public void webviewGoBack() {
        if(webView.canGoBack()){
            webView.goBack();
        }
    }

    private void setInitialUrl() {
        if(getIntent().hasExtra("launchURL")){
            currentUrl = getIntent().getStringExtra("launchURL");
            return;
        }

        if(!Settings.OPEN_LOCAL_HTML_BY_DEFAULT){
            setOnlineHomeUrl();
            String strData = LinkUtil.checkUniversalLink(this);
            checkOpenSpecialLinkOnline(strData);
        }
        else{
            setOfflineHomeUrl();
            String strData = LinkUtil.checkUniversalLink(this);
            checkOpenSpecialLinkOffline(strData);
        }
    }

    private void setOnlineHomeUrl() {
        showingLocalWebsite = false;
        currentUrl = Settings.HOME_URL;
        if (Settings.PUSH_ENABLED) {
            // get push token
            OSPermissionSubscriptionState status = OneSignal.getPermissionSubscriptionState();
            userId = status.getSubscriptionStatus().getUserId();
            LogUtil.loge("userId: "+userId);
            if(currentUrl.contains("?")){
                currentUrl = currentUrl + "&player_id=" + userId;
            }
            else {
                currentUrl = currentUrl + "?player_id=" + userId;
            }
        }
        webView.clearHistory();
    }

    private void setOfflineHomeUrl() {
        showingLocalWebsite = true;
        currentUrl = "file:///android_asset/website/"+Settings.LOCAL_HTML_INDEX_PAGE;
        webView.clearHistory();
    }

    private void checkOpenSpecialLinkOnline(String strData){
        if(strData == null)
            return;
        String [] arr = strData.split("//");
        if(arr.length > 1){
            // open online specific page
            currentUrl = Settings.HOME_URL
                    .replace("?","")
                    .replace("/saifal.php","")
                    +"/"+arr[1];
        }
        else{
            // open online home page
            currentUrl = Settings.HOME_URL;
        }
        showingLocalWebsite = false;
    }

    private void checkOpenSpecialLinkOffline(String strData){
        if(strData == null)
            return;
        String [] arr = strData.split("//");
        if(arr.length > 1){
            // open offline specific page
            currentUrl = "file:///android_asset/website/"+arr[1];
        }
        else{
            // open offline home page
            currentUrl = "file:///android_asset/website/"+Settings.LOCAL_HTML_INDEX_PAGE;
        }
        showingLocalWebsite = true;
    }

    public void showContent(){
        if(Settings.SHOW_DRAWER){
            DrawerLayout drawerLayout = findViewById(R.id.drawer_layout);
            drawerLayout.setVisibility(View.VISIBLE);
        }
        if(!pullToRefresh.isShown())
            pullToRefresh.setVisibility(View.VISIBLE);
    }

    public void hideContent(){
        if(Settings.SHOW_DRAWER){
            DrawerLayout drawerLayout = findViewById(R.id.drawer_layout);
            drawerLayout.setVisibility(View.GONE);
        }
        pullToRefresh.setVisibility(View.GONE);
    }

    private void setStatusBarColor() {
        Utils.changeStatusBarColor(this, getResources().getColor(R.color.statusBarColor));
    }

    private void setPulltoRefresh() {
        pullToRefresh.setEnabled(Settings.PULL_TO_REFRESH);
        int color = getResources().getColor(R.color.loadingSignColor);
        pullToRefresh.setColorSchemeColors(color, color, color);
        pullToRefresh.setProgressViewOffset(false, 0 , (int)Utils.convertDpToPixel(Settings.PULL_TO_REFRESH_POSITION_FROM_TOP, this));
        pullToRefresh.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                LogUtil.loge("onRefresh");
                loadWebPage();
            }
        });
        pullToRefresh.getViewTreeObserver().addOnScrollChangedListener(new ViewTreeObserver.OnScrollChangedListener() {
            @Override
            public void onScrollChanged() {
                if (webView.getScrollY() == 0)
                    pullToRefresh.setEnabled(Settings.PULL_TO_REFRESH);
                else
                    pullToRefresh.setEnabled(false);
            }
        });
    }

    private void setupWebView(WebView webView, boolean isPopup) {
        if(!Settings.USER_AGENT.isEmpty())
            webView.getSettings().setUserAgentString(Settings.USER_AGENT);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setSupportZoom(true);
        webView.getSettings().setBuiltInZoomControls(false);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowFileAccessFromFileURLs(true);
        webView.getSettings().setAllowUniversalAccessFromFileURLs(true);
        webView.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setSupportMultipleWindows(true);
        webView.getSettings().setPluginState(WebSettings.PluginState.ON);
        webView.getSettings().setAppCacheEnabled(Settings.CACHE_ENABLED);
        webView.getSettings().setMediaPlaybackRequiresUserGesture(false);
        webView.setWebViewClient(new MyWebViewClient(isPopup));
        webView.setWebChromeClient(new MyWebChromeClient());
        webView.setDownloadListener(new TestDownloadManager());
        webView.addJavascriptInterface(new MyJavaScriptInterface(Home.this), "Android");
    }

    String downloadUrl = "";
    String contentDisposition = "";
    String mimeType = "";
    private long downloadReference;

    private class TestDownloadManager implements DownloadListener {
        public void onDownloadStart(String url, String userAgent, String contDis, String mtype, long contentLength) {
            LogUtil.loge("onDownloadStart: "+url);
            downloadUrl = url;
            contentDisposition = contDis;
            mimeType = mtype;
            if(PermissionUtil.checkDownloadPermission(Home.this)) {
                downloadFile();
            }
            else{
                PermissionUtil.getDownloadPermission(Home.this);
            }
        }
    }

    private void downloadFile() {
        if(downloadUrl.isEmpty())
            return;
        Toast.makeText(Home.this, getResources().getString(R.string.downloading), Toast.LENGTH_SHORT).show();
        DownloadManager downloadManager = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
        DownloadManager.Request request = new DownloadManager.Request(Uri.parse(downloadUrl));
        String fileName = URLUtil.guessFileName(downloadUrl, contentDisposition, mimeType);
        LogUtil.loge("fileName: "+fileName);
        request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName);
        request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
        //request.setTitle(title);
        //request.setDescription(desc);
        request.setMimeType(mimeType);
        downloadReference = downloadManager.enqueue(request);
        IntentFilter filter = new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE);
        registerReceiver(downloadReceiver, filter);
    }

    private BroadcastReceiver downloadReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            //check if the broadcast message is for our enqueued download
            long referenceId = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
            if (referenceId == downloadReference) {
                LogUtil.loge("open file");
                IntentUtil.openDownloadedAttachment(context, referenceId);
                unregisterReceiver(this);
            }
        }
    };

    public void loadWebPageFromBottomMenu(String url) {
        LogUtil.loge("load: "+url);
        currentUrl = url;
        if(currentUrl != null) {
            if(!currentUrl.isEmpty()) {
                showProgress();
                webView.loadUrl(currentUrl);
            }
        }
    }

    public void loadWebPageFromDrawer(String url) {
        LogUtil.loge("load: "+url);
        drawerUtil.drawerToggle();
        currentUrl = url;
        if(currentUrl != null) {
            if(!currentUrl.isEmpty()) {
                showProgress();
                webView.loadUrl(currentUrl);
            }
        }
    }

    public void loadWebPage() {
        if(currentUrl != null) {
            if(!currentUrl.isEmpty()) {
                if(homeLoaded)
                    showProgress();
                webView.loadUrl(currentUrl);
            }
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    private void grantedVideoCapturePermission() {
        LogUtil.loge("grantedVideoCapturePermission");
        permissionRequest.grant(permissionRequest.getResources());
    }

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            if (requestCode == LOC_PERMISSION) {
                if (mGeoLocationCallback != null)
                    mGeoLocationCallback.invoke(mGeoLocationRequestOrigin, true, true);
            }
            else if(requestCode == VIDEO_CAPTURE_PERMISSION1){
                if(!PermissionUtil.checkAudioPermission(Home.this)){
                    PermissionUtil.getAudioPermission(Home.this);
                }
                else{
                    grantedVideoCapturePermission();
                }
            }
            else if(requestCode == VIDEO_CAPTURE_PERMISSION2){
                grantedVideoCapturePermission();
            }
            else if(requestCode == DOWNLOAD_PERMISSION){
                downloadFile();
            }
            else if(requestCode == READ_PERMISSION){
                FilePicker.openChooser(Home.this);
            }
            else if(requestCode == WRITE_PERMISSION){
                FilePicker.openChooser(Home.this);
            }
            else if(requestCode == CAMERA_PERMISSION){
                FilePicker.openChooser(Home.this);
            }
        }
    }

    private class MyWebChromeClient extends WebChromeClient{
        @Override
        public boolean onCreateWindow(WebView view, boolean isDialog, boolean isUserGesture, Message resultMsg) {
            LogUtil.loge("onCreateWindow");
            LogUtil.loge("isDialog: "+isDialog);
            LogUtil.loge("isUserGesture: "+isUserGesture);
//            if(!isDialog){
//                 //_blank link
//                WebView.HitTestResult result = view.getHitTestResult();
//                String data = result.getExtra();
//                if(data != null){
//                    currentUrl = data;
//                    loadWebPage();
//                }
//                else{
//                    LogUtil.loge("data NULL");
//                }
//                return false;
//            }
            mWebviewPop = new WebView(Home.this);
            setupWebView(mWebviewPop, true);
            mWebviewPop.setLayoutParams(new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
            container.addView(mWebviewPop);
            WebView.WebViewTransport transport = (WebView.WebViewTransport) resultMsg.obj;
            transport.setWebView(mWebviewPop);
            resultMsg.sendToTarget();
            return true;
        }

        @Override
        public void onCloseWindow(WebView window) {
            LogUtil.loge("onCloseWindow");
        }

        @Override
        public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
            LogUtil.loge("onGeolocationPermissionsShowPrompt");
            if (ContextCompat.checkSelfPermission(Home.this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(Home.this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, LOC_PERMISSION);
                mGeoLocationRequestOrigin = origin;
                mGeoLocationCallback = callback;
            }
            else{
                callback.invoke(origin, true, true);
            }
        }

        @Override
        public void onPermissionRequest(PermissionRequest request) {
            LogUtil.loge("onPermissionRequest");
            permissionRequest = request;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                for(String permission: request.getResources()){
                    if(permission.equals(PermissionRequest.RESOURCE_VIDEO_CAPTURE)){
                        if (ContextCompat.checkSelfPermission(Home.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                            ActivityCompat.requestPermissions(Home.this, new String[]{Manifest.permission.CAMERA}, VIDEO_CAPTURE_PERMISSION1);
                        }
                        else if (ContextCompat.checkSelfPermission(Home.this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                            ActivityCompat.requestPermissions(Home.this, new String[]{Manifest.permission.RECORD_AUDIO}, VIDEO_CAPTURE_PERMISSION2);
                        }
                        else{
                            grantedVideoCapturePermission();
                        }
                    }
                }
            }
        }

        // For Lollipop 5.0+ Devices
        @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
        public boolean onShowFileChooser(WebView mWebView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
            //String acceptTypes[] = fileChooserParams.getAcceptTypes();
            if (mFilePathCallback != null) {
                mFilePathCallback.onReceiveValue(null);
            }
            mFilePathCallback = filePathCallback;
            FilePicker.openChooser(Home.this);
            return true;
        }

        //For Android 4.1 only
        protected void openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType, String capture) {
            LogUtil.loge("types: "+acceptType);
            mUploadMessage = uploadMsg;
            FilePicker.openChooser(Home.this);
        }

        protected void openFileChooser(ValueCallback<Uri> uploadMsg) {
            mUploadMessage = uploadMsg;
            FilePicker.openChooser(Home.this);
        }

        // full screen video
        private View mCustomView;
        private WebChromeClient.CustomViewCallback mCustomViewCallback;
        protected FrameLayout mFullscreenContainer;
        private int mOriginalOrientation;
        private int mOriginalSystemUiVisibility;

        public Bitmap getDefaultVideoPoster() {
            return BitmapFactory.decodeResource(Home.this.getApplicationContext().getResources(), 2130837573);
        }

        public void onHideCustomView() {
            ((FrameLayout)Home.this.getWindow().getDecorView()).removeView(this.mCustomView);
            this.mCustomView = null;
            Home.this.getWindow().getDecorView().setSystemUiVisibility(this.mOriginalSystemUiVisibility);
            Home.this.setRequestedOrientation(this.mOriginalOrientation);
            this.mCustomViewCallback.onCustomViewHidden();
            this.mCustomViewCallback = null;
        }

        public void onShowCustomView(View paramView, WebChromeClient.CustomViewCallback paramCustomViewCallback) {
            if (this.mCustomView != null) {
                onHideCustomView();
                return;
            }
            this.mCustomView = paramView;
            this.mOriginalSystemUiVisibility = Home.this.getWindow().getDecorView().getSystemUiVisibility();
            this.mOriginalOrientation = Home.this.getRequestedOrientation();
            this.mCustomViewCallback = paramCustomViewCallback;
            ((FrameLayout)Home.this.getWindow().getDecorView()).addView(this.mCustomView, new FrameLayout.LayoutParams(-1, -1));
            Home.this.getWindow().getDecorView().setSystemUiVisibility(3846);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult r = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if(r != null) {
            if(r.getContents() == null) {
                //
            }
            else {
                String scanned = r.getContents();
                Toast.makeText(this, "Scanned: "+scanned, Toast.LENGTH_LONG).show();
                if (!Settings.OPEN_SCAN_URL_IN_WEBVIEW) {
                    Utils.openUrlInChrome(Home.this, scanned);
                }
                else{
                    currentUrl = scanned;
                    loadWebPage();
                }
            }
        }

        // when photo is selected gallery/camera
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            if (requestCode != FILECHOOSER_RESULTCODE || mFilePathCallback == null) {
                super.onActivityResult(requestCode, resultCode, data);
                return;
            }
            Uri[] results = null;
            // Check that the response is a good one
            if (resultCode == Activity.RESULT_OK) {
                if (data == null) {
                    if (mPhotoCapturedURI != null) {
                        results = new Uri[]{mPhotoCapturedURI};
                        LogUtil.loge("camera results: "+results[0]);
                    }
                }
                else {
                    if(data.getData() == null){
                        if (mPhotoCapturedURI != null) {
                            results = new Uri[]{mPhotoCapturedURI};
                            LogUtil.loge("camera results: "+results[0]);
                        }
                    }
                    else{
                        String dataString = data.getDataString();
                        if (dataString != null) {
                            results = new Uri[]{Uri.parse(dataString)};
                            LogUtil.loge("gallery results: "+results[0]);
                        }
                    }
                }
            }
            mFilePathCallback.onReceiveValue(results);
            mFilePathCallback = null;
        }
        else if (Build.VERSION.SDK_INT <= Build.VERSION_CODES.KITKAT) {
            if (requestCode != FILECHOOSER_RESULTCODE || mUploadMessage == null) {
                super.onActivityResult(requestCode, resultCode, data);
                return;
            }
            if (requestCode == FILECHOOSER_RESULTCODE) {
                if (null == this.mUploadMessage) {
                    return;
                }
                Uri result = null;
                try {
                    if (resultCode != RESULT_OK) {
                        result = null;
                    } else {
                        // retrieve from the private variable if the intent is null
                        result = data == null ? mPhotoCapturedURI : data.getData();
                    }
                } catch (Exception e) {
                    Toast.makeText(getApplicationContext(), "activity :" + e, Toast.LENGTH_LONG).show();
                }
                mUploadMessage.onReceiveValue(result);
                mUploadMessage = null;
            }
        }
    }

    private class MyWebViewClient extends WebViewClient {
        boolean isPopup;

        public MyWebViewClient(boolean isPopup){
            this.isPopup = isPopup;
        }

        @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            String url = request.getUrl().toString();
            LogUtil.loge("shouldOverrideUrlLoading1: " + url);
            return handleOverrideUrl(url);
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            LogUtil.loge("shouldOverrideUrlLoading2: " + url);
            return handleOverrideUrl(url);
        }

        @Override
        public void onPageStarted(WebView view, String url, Bitmap favicon) {
            super.onPageStarted(view, url, favicon);
            LogUtil.loge("loading: " + url);
            currentUrl = url;

            if(homeLoaded) {
                LogUtil.loge("show progress");
                showProgress();
            }

            if(!NetworkUtil.isInternetOn(Home.this)) {
                showNoInternet(true);
                hideProgress();
            }
            else {
                showNoInternet(false);
            }
        }

        @Override
        public void doUpdateVisitedHistory(WebView view, String url, boolean isReload) {
            super.doUpdateVisitedHistory(view, url, isReload);
            LogUtil.loge("doUpdateVisitedHistory: "+url);
            currentUrl = url;
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);
            LogUtil.loge("finished: " + url);
            //String cookies = CookieManager.getInstance().getCookie(url);
            //LogUtil.loge("cookies:" + cookies);
            hideProgress();

            if (url.contains(target_url_prefix)) {
                LogUtil.loge("1");
                if(!isPopup)
                    closeWebviewPopup();
            }

            if(url.endsWith("/logout")){
                LogUtil.loge("2");
                if(!isPopup)
                    closeWebviewPopup();
                setInitialUrl();
                loadWebPage();
                return;
            }

            if(Settings.INJECT_CSS)
                InjectUtil.injectCSS(Home.this, view, "website/css/"+Settings.INJECT_CSS_FILENAME);
            if(Settings.INJECT_JS)
                InjectUtil.injectScriptFile(Home.this, view, "website/js/"+Settings.INJECT_JS_FILENAME);

            if(Settings.SHOW_DRAWER){
                if(webView.canGoBack()){
                    drawerUtil.showBack();
                }
                else{
                    drawerUtil.hideBack();
                }
            }

            // check if home url loaded (1st url)
            if(!homeLoaded){
                homeLoaded = true;
            }
        }

        private boolean handleOverrideUrl(String url) {
            linkClicks++;
            if(linkClicks >= Settings.INTERSTITIAL_AD_AFTER_CLICKS){
                AdUtil.loadInterstitialAd(Home.this);
            }
            String host = Uri.parse(url).getHost();
            LogUtil.loge("host: "+host);

            if(url.startsWith("qrcode://")){
                openQrScanner();
                return true;
            }
            else if(url.startsWith("ratedialog://")){
                RateDialogUtil.showRateDialog(Home.this);
                return true;
            }
            else if(url.startsWith("reset://")){
                clearCache();
                return true;
            }
            else if(url.startsWith("enablepush://")){
                PrefsUtil.setPushEnabled(Home.this, true);
                return true;
            }
            else if(url.startsWith("disablepush://")){
                PrefsUtil.setPushEnabled(Home.this, false);
                return true;
            }
            else if(url.startsWith("inapp://")){
                String [] arr = url.split("//");
                if(arr.length > 1){
                    String productId = arr[1];
                    inAppBilling.makePurchase(productId);
                }
                return true;
            }
            else if(url.startsWith(getString(R.string.universalLink))){
                if(!Settings.OPEN_LOCAL_HTML_BY_DEFAULT){
                    checkOpenSpecialLinkOnline(url);
                }
                else{
                    checkOpenSpecialLinkOffline(url);
                }
                loadWebPage();
                return true;
            }
            else if(!url.startsWith("file:///android_asset")
                    && !url.startsWith("http")
                    && !url.startsWith("https")) {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                startActivity(intent);
                return true;
            }
            else if(url.contains("play.google.com")){
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                startActivity(intent);
                return true;
            }
            else if(url.startsWith("https://web.facebook.com/dialog/close_window")){
                setInitialUrl();
                loadWebPage();
                return true;
            }
            else if(url.startsWith("https://accounts.google.com/signin")){
                LogUtil.loge("3");
                if(!isPopup)
                    closeWebviewPopup();
                return false;
            }
            else if (host.contains(target_url_prefix)) {
                LogUtil.loge("4");
                if(!isPopup)
                    closeWebviewPopup();
                return false;
            }

            if(!Settings.OPEN_LOCAL_HTML_BY_DEFAULT) {
                if (!url.contains(Settings.HOST)) {
                    if (Settings.OPEN_EXTERNAL_LINKS_IN_BROWSER) {
                        for (String whitelistExternalUrl : Settings.WHITELIST_EXTERNAL_URLS) {
                            if(url.equals(whitelistExternalUrl)){
                                return false;
                            }
                        }
                        Utils.openUrlInChrome(Home.this, url);
                        return true;
                    }
                }
            }
            return false;
        }
    }

    private void closeWebviewPopup() {
        if (mWebviewPop != null) {
            LogUtil.loge("remove webview popup");
            mWebviewPop.setVisibility(View.GONE);
            container.removeView(mWebviewPop);
            mWebviewPop = null;
        }
    }

    private void openQrScanner() {
        new IntentIntegrator(this).initiateScan();
    }

    public void clearCache() {
        LogUtil.loge("clearCache");
        WebStorage.getInstance().deleteAllData();
        webView.clearCache(true);
        webView.clearFormData();
        webView.clearHistory();
        webView.clearSslPreferences();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP_MR1) {
            CookieManager.getInstance().removeAllCookies(null);
            CookieManager.getInstance().flush();
        }
        else {
            CookieSyncManager cookieSyncMngr = CookieSyncManager.createInstance(Home.this);
            cookieSyncMngr.startSync();
            CookieManager cookieManager = CookieManager.getInstance();
            cookieManager.removeAllCookie();
            cookieManager.removeSessionCookie();
            cookieSyncMngr.stopSync();
            cookieSyncMngr.sync();
        }
        String cookies = CookieManager.getInstance().getCookie(currentUrl);
        LogUtil.loge("cookies after clear: "+cookies);
    }

    private void showNoInternet(boolean offline) {
        if(Settings.OPEN_LOCAL_HTML_BY_DEFAULT){
            return;
        }

        if(offline){
            if(Settings.OPEN_LOCAL_HTML_WHEN_OFFLINE){
                if(showingLocalWebsite){
                    // already showing local website
                    return;
                }
                setOfflineHomeUrl();
                loadWebPage();
            }
            else{
                noInternet.setVisibility(View.VISIBLE);
            }
        }
        else{
            noInternet.setVisibility(View.GONE);
            if(showingLocalWebsite){
                // if previously showing local website now load online website
                setOnlineHomeUrl();
                loadWebPage();
            }
        }
    }

    public void showProgress(){
        if(Settings.LOADING_SIGN)
            pullToRefresh.setRefreshing(true);
    }

    public void hideProgress(){
        pullToRefresh.setRefreshing(false);
    }

    @Override
    public void onBackPressed() {
        if(mWebviewPop != null) {
            if(mWebviewPop.canGoBack()){
                mWebviewPop.goBack();
                return;
            }
            closeWebviewPopup();
            return;
        }

        if(webView.canGoBack()){
            webviewGoBack();
            return;
        }

        super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(CloseHome);
        timerUtil.stopTimer();
        if(!Settings.CACHE_ENABLED)
            webView.destroy();
    }

    private BroadcastReceiver CloseHome = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            finish();
        }
    };

    @Override
    public void onConfigurationChanged(@NonNull Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        AdUtil.loadBannerAd(Home.this, adParent);
    }

}