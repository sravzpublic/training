
import UIKit
import WebKit
import StoreKit
import AVFoundation
import OneSignal
import StoreKit
import GoogleMobileAds

class HomeController: UITabBarController, WKUIDelegate, WKNavigationDelegate, UIDocumentInteractionControllerDelegate, UIGestureRecognizerDelegate, QrDelegate {
    // MARK: - Properties
    var webViewContainer: UIView!
    var no_internetContainer: UIView!
    var no_internet: UIImageView!
    var no_internetLabel: UILabel!
    var activityIndicator: UIActivityIndicatorView!
    var backButton: UIButton!
    var tapDetectorView: UIView!
    var navGestureDetector: UIGestureRecognizer!
    var bannerContainer: UIView!
    
    var bannerView: GADBannerView!
    var interstitial: GADInterstitial!
    var clickCount = 0
    
    var webView: WKWebView!
    var refreshControl:UIRefreshControl?
    
    var homeDelegate: HomeControllerDelegate?
        
    public var webURL = Settings.OPEN_LOCAL_HTML_BY_DEFAULT ? Settings.LOCAL_HTML_INDEX_PAGE : Settings.URL
    private var orientation = Settings.ORIENTATION
    private var statusBarColor = Settings.STATUS_BAR_COLOR
    private var statusBarTextMode = Settings.STATUS_BAR_TEXT_COLOR
    
    private var isPulled = false
    private var wasOffline = false
    private var refreshURL:URL = URL(string: Settings.URL)!
    private var appCount = UserDefaults.standard.integer(forKey: "count")
    public var launchURL:Any?
    private var isLaunchURL = false
    private var isLinkClicked = false
    private var isCssInjected = false
    private var isJSInjected = false
    private var isScannedURL = false
    private var isMenuLinkTapped = false
    public var passedUrl: String? {
        didSet{
            loadWebWithUrlString(url: passedUrl!, webView: webView)
            DispatchQueue.main.asyncAfter(deadline: .now()+0.21) {
                self.setWebViewContainerHeight(isOpenFromBrowser: true)
            }
        }
    }
    
    private var qrUrl: String? {
        didSet {
            isScannedURL = true
            loadWebWithUrlString(url: qrUrl!, webView: webView)
        }
    }
    var menuURL: String? {
        didSet{
            isMenuLinkTapped = true
            removeGestureDetectors()
            activityIndicator.startAnimating()
            loadWebWithUrlString(url: menuURL!, webView: webView)
        }
    }
    private var tabBarHeight: CGFloat?
    private var navbarHeight: CGFloat?
    private var statusBarHeight: CGFloat? {
        didSet {
            setWebViewContainerHeight()
        }
    }
    
// MARK: - Init
    override func viewDidLoad() {
        super.viewDidLoad()
        createAndLoadInterstitial()
        
        findHeights()
        configureNavigationBar()
        
        initViews()
        
        pushLaunchURL()
        deepLinking()
        
        wasOffline = !isConnected()
        webContainerLoad()
        
        rateDialogAppearance()
        configureTabBar()
        
        SKPaymentQueue.default().add(self)
        
    }
    
    func initViews(){
        webViewContainer = UIView()
        webViewContainer.frame = CGRect(x: 0, y: 0, width: view.frame.width, height: view.frame.height)
        view.addSubview(webViewContainer)
        
        let w = view.frame.width
        let h = view.frame.height
        
        no_internet = UIImageView()
        no_internet.image = #imageLiteral(resourceName: "no_internet")
        no_internet.frame = CGRect(x: w/2 - 55, y: h/3, width: 110, height: 70)
        view.addSubview(no_internet)
        
        no_internetLabel = UILabel()
        no_internetLabel.numberOfLines = 2
        no_internetLabel.textAlignment = .center
        no_internetLabel.text = "No internet connection. Please connect and try again"
        no_internetLabel.frame = CGRect(x: w/2 - 125, y: h/3 + 80, width: 250, height: 50)
        view.addSubview(no_internetLabel)
        
        activityIndicator = UIActivityIndicatorView()
        activityIndicator.transform = CGAffineTransform(scaleX: 1.5, y: 1.5)
        view.addSubview(activityIndicator)
        activityIndicator.inCenterOf(superview: view, width: 200, height: 200)
        
    }
    
    private func adBannerSetup(){
        bannerContainer = UIView()
        bannerContainer.backgroundColor = .lightGray
        view.addSubview(bannerContainer)
        
        let containerLabel = UILabel()
        containerLabel.text = "Banner Ad"
        containerLabel.frame = CGRect(x: view.frame.size.width/2 - 50, y: calculateBannerHeight()/2 - 17, width: 120, height: 35)
        bannerContainer.addSubview(containerLabel)
        
        bannerContainer.translatesAutoresizingMaskIntoConstraints = false
        bannerContainer.leadingAnchor.constraint(equalTo: webViewContainer.leadingAnchor).isActive = true
        bannerContainer.topAnchor.constraint(equalTo: webViewContainer.bottomAnchor).isActive = true
        bannerContainer.trailingAnchor.constraint(equalTo: webViewContainer.trailingAnchor).isActive = true
        bannerContainer.heightAnchor.constraint(equalToConstant: calculateBannerHeight()).isActive = true
        
        print("Banner Height: \(calculateBannerHeight())")
        bannerView = GADBannerView(adSize: kGADAdSizeBanner)
        bannerView.adUnitID = Settings.ADMOB_BANNER_ID
        bannerView.rootViewController = self
        bannerContainer.addSubview(bannerView)
        bannerView.placeIn(superView: bannerContainer)
        
        bannerView.delegate = self
        bannerView.load(GADRequest())
    }
    
    func createAndLoadInterstitial() {
        if Settings.INTERSTITIAL_AD {
            interstitial = GADInterstitial(adUnitID: Settings.ADMOB_INTERSTITIAL_ID)
            interstitial.delegate = self
            interstitial.load(GADRequest())
        }
    }
    
    func showInterstitialAd(){
        if interstitial.isReady {
          interstitial.present(fromRootViewController: self)
        } else {
          print("Ad wasn't ready")
        }
    }

    func interstitialDidDismissScreen(_ ad: GADInterstitial) {
        createAndLoadInterstitial()
    }
    
    // MARK: - Handlers
    private func tapDetectorViewSetup(){
        if !isExpanded {
            tapDetectorView = UIView()
            
            view.addSubview(tapDetectorView)
            tapDetectorView.placeIn(superView: view)
            
            let gestureDetector = UITapGestureRecognizer(target: self, action: #selector(hideMenu))
            gestureDetector.delegate = self
            tapDetectorView.addGestureRecognizer(gestureDetector)
            
            navGestureDetector = UITapGestureRecognizer(target: self, action: #selector(hideMenu))
            navGestureDetector.delegate = self
            navigationController?.navigationBar.addGestureRecognizer(navGestureDetector)
        } else {
            removeGestureDetectors()
        }
    }
    
    private func removeGestureDetectors(){
        if tapDetectorView != nil {tapDetectorView.removeFromSuperview()}
        if navGestureDetector != nil {
            navigationController?.navigationBar.removeGestureRecognizer(navGestureDetector)
        }
    }
    
    private func findHeights(){
        DispatchQueue.main.asyncAfter(deadline: .now()+0.2) {
            if #available(iOS 13.0, *) {
                self.tabBarHeight = self.tabBar.frame.size.height
                self.navbarHeight = self.navigationController?.navigationBar.frame.height
                self.statusBarHeight = self.view.window?.windowScene?.statusBarManager?.statusBarFrame.height
            } else {
                self.tabBarHeight = self.tabBar.frame.size.height
                self.navbarHeight = self.navigationController?.navigationBar.frame.height
                self.statusBarHeight = UIApplication.shared.statusBarFrame.size.height
            }
        }
    }
    
    private func setWebViewContainerHeight(isOpenFromBrowser: Bool = false){
        if tabBarHeight != nil {
            
            if UserDefaults.standard.double(forKey: "tabbarHeight") == 0 {
                UserDefaults.standard.set(tabBarHeight, forKey: "tabbarHeight")
            }
            
            if isOpenFromBrowser {tabBarHeight = CGFloat(UserDefaults.standard.double(forKey: "tabbarHeight"))}
            
            let yPoint = Settings.SHOW_DRAWER ? (statusBarHeight ?? 40) + (navbarHeight ?? 40) : statusBarHeight
            
            var bottomPadding = Settings.SHOW_BOTTOM_MENU ? ((tabBarHeight ?? 10) + (yPoint ?? 40)) : yPoint ?? 40
            
            if Settings.BANNER_AD {
                bottomPadding = bottomPadding + calculateBannerHeight()
            }
            
            webViewContainer.frame = CGRect(x: 0, y: yPoint ?? 40, width: view.frame.width, height: view.frame.height - bottomPadding)
            
            if Settings.BANNER_AD { adBannerSetup() }
            
        }
    }
    
    private func genererateNavController(title: String, image: String) -> UIViewController{
        let navController = UIViewController()
        navController.title = title
        if Settings.SHOW_BOTTOM_MENU_ICONS {
            let img = UIImage(named: image)
            navController.tabBarItem.image = img
        }
        return navController
    }
    
    private func configureNavigationBar(){
        navigationController?.navigationBar.barTintColor = Settings.TITLEBAR_BACKGROUND_COLOR
        let textAttributes = [NSAttributedString.Key.foregroundColor:Settings.TITLEBAR_TINT_COLOR == "white" ? UIColor.white : UIColor.black]
        navigationController?.navigationBar.titleTextAttributes = textAttributes
        
        navigationItem.title = "Convertify"
        addNavigationBarItems()
    }
    
    private func configureTabBar(){
        addTabItems()
        tabBar.barTintColor = Settings.BOTTOM_MENU_BACKGROUND_COLOR
        tabBar.tintColor = Settings.BOTTOM_MENU_SELECTED_ITEM_COLOR
        tabBar.unselectedItemTintColor = Settings.BOTTOM_MENU_UNSELECTED_ITEM_COLOR
        tabBar.isHidden = !Settings.SHOW_BOTTOM_MENU
    }
    
    private func addTabItems(){
        var vcs: [UIViewController] = []
        var index = 0
        Settings.BOTTOM_MENU_TITLES.forEach { (title) in
            if index < 5 {
                let vc = genererateNavController(title: title, image: Settings.BOTTOM_MENU_ICONS[index])
                vcs.append(vc)
                index += 1
            } else {
                print("tabs else called")
            }
        }
        viewControllers = vcs
    }
    
    @objc func handleMenu(){
        tapDetectorViewSetup()
        if let delegate = homeDelegate {
            delegate.handleMenuToggle(forIndex: nil)
        }
    }
    
    @objc func hideMenu(){
        removeGestureDetectors()
        if let delegate = homeDelegate {
            delegate.handleMenuToggle(forIndex: nil)
        }
    }
    
    @objc func backButtonPressed(){
        if webView.canGoBack {
            webView.goBack()
        }
    }
    
    @objc func refreshButtonPressed(){
        webView.reload()
    }

    
    private func addNavigationBarItems(){
        let menuButton = UIButton(type: .system)
        setButtonProperties(target: self, button: menuButton, image: "menu", objFunc: #selector(handleMenu))
        
        let menuItem = UIBarButtonItem(customView: menuButton)
        setBarItemProperties(item: menuItem)
        
        backButton = UIButton(type: .system)
        setButtonProperties(target: self, button: backButton, image: "back", objFunc: #selector(backButtonPressed))
        
        let backItem = UIBarButtonItem(customView: backButton)
        setBarItemProperties(item: backItem)
        
        let refreshButton = UIButton(type: .system)
        setButtonProperties(target: self, button: refreshButton, image: "refresh", objFunc: #selector(refreshButtonPressed))
        
        let refreshItem = UIBarButtonItem(customView: refreshButton)
        setBarItemProperties(item: refreshItem)
        
        navigationItem.leftBarButtonItems = [menuItem, backItem]
        navigationItem.rightBarButtonItem = refreshItem
        backButton.isHidden = true
    }
    
    func gestureRecognizer(_ gestureRecognizer: UIGestureRecognizer, shouldRecognizeSimultaneouslyWith otherGestureRecognizer: UIGestureRecognizer) -> Bool {
        print("expanded: \(isExpanded)")
        if isExpanded {
          return true
        } else {
          return false
        }
    }
    
    private func doInjections(){
        if Settings.INJECT_CSS {
            injectCssToPage(webView: webView, name: Settings.INJECT_CSS_FILENAME)
        }
        if Settings.INJECT_JS {
            injectJsToPage(webView: webView, name: Settings.INJECT_JS_FILENAME)
        }
    }
    
    private func pushLaunchURL(){
        launchURL = UserDefaults.standard.object(forKey: "launchURL")
        if launchURL != nil {
            print("not nil")
            webURL = launchURL as! String
            UserDefaults.standard.set(nil, forKey: "launchURL")
            isLaunchURL = true
        }else{
            print("url is nil")
        }
    }
    
    private func deepLinking(){
        if Settings.PUSH_ENABLED {
            OneSignal.add(self as OSSubscriptionObserver)
            let status = OneSignal.getPermissionSubscriptionState()
            let isAllowed = UserDefaults.standard.bool(forKey: "isAllowed")
            print("Allowed: \(isAllowed)")
            var userId:String?
            for i in 1...20 {
                userId = status?.subscriptionStatus.userId
                print("loop \(i) time called: user id: \(userId ?? "")")
                if userId != nil {
                    if isAllowed {
                        if webURL.contains("?"){
                            webURL = webURL + "&player_id=" + userId!
                        }else{
                            webURL = webURL + "?player_id=" + userId!
                        }
                        print("weburl: \(webURL)")
                    }
                    return
                }
            }
        }
    }
    
    private func loadWebView(urlRequest: URLRequest){
        if isConnected() {
            no_internet.isHidden = true
            no_internetLabel.isHidden = true
            webView.load(urlRequest)
            activityNavigator()
        }
        else if !isConnected() && Settings.OPEN_LOCAL_HTML_WHEN_OFFLINE {
            webURL = Settings.LOCAL_HTML_INDEX_PAGE
            let myURL = createURL(url: webURL)
            let myRequest = URLRequest(url: myURL)
            no_internet.isHidden = true
            no_internetLabel.isHidden = true
            webView.load(myRequest)
            activityNavigator()
        }
        else if !((Settings.URL).localizedCaseInsensitiveContains("http")){
            no_internet.isHidden = true
            no_internetLabel.isHidden = true
            webView.load(urlRequest)
            activityNavigator()
        }
        
        else {
            no_internet.isHidden = false
            no_internetLabel.isHidden = false
        }
    }
    
    private func webContainerLoad(){
        setWebView()
        webViewContainer.addSubview(no_internetLabel)
        webViewContainer.addSubview(no_internet)
        print("WebUrlToLoad: \(webURL)")
        let myURL = createURL(url: webURL)
        let myRequest = URLRequest(url: myURL)
        loadWebView(urlRequest: myRequest)
        pullToRefresh()
    }
    
    // rate dialog
    private func rateDialogAppearance(){
        if Settings.RATE_DIALOG{
            let count = Settings.RATE_DIALOG_AFTER_APP_LAUNCHES
            if appCount >= count {
                if #available( iOS 10.3,*){
                    SKStoreReviewController.requestReview()
                }
                appCount = 1
                UserDefaults.standard.set(appCount, forKey: "count")
            }
            else{
                appCount = appCount + 1
                UserDefaults.standard.set(appCount, forKey: "count")
            }
        }
    }

    // MARK: - Setting up the webview
    private func setWebView(){
        
        let webConfiguration = WKWebViewConfiguration()
        
        webConfiguration.allowsInlineMediaPlayback = true

       let customFrame = CGRect.init(origin: CGPoint.zero, size: CGSize.init(width: 0.0, height: self.webViewContainer.frame.size.height))

        self.webView = WKWebView (frame: customFrame , configuration: webConfiguration)
        self.webViewContainer.addSubview(webView)
        
        //self.webView.placeIn(superView: webViewContainer)
        //self.webView.frame = self.webViewContainer!.bounds
        
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.topAnchor.constraint(equalTo: webViewContainer.topAnchor).isActive = true
        webView.rightAnchor.constraint(equalTo: webViewContainer.rightAnchor).isActive = true
        webView.leftAnchor.constraint(equalTo: webViewContainer.leftAnchor).isActive = true
        webView.bottomAnchor.constraint(equalTo: webViewContainer.bottomAnchor, constant: 20).isActive = true
        webView.heightAnchor.constraint(equalTo: webViewContainer.heightAnchor).isActive = true
        
        if #available(iOS 11.0, *) {
            webView.scrollView.contentInsetAdjustmentBehavior = .never
        }
    
        webView.uiDelegate = self
        webView.navigationDelegate = self
        webView.allowsBackForwardNavigationGestures = Settings.ALLOW_BACKWARD_FORWARD_GESTURE
        webView.customUserAgent = Settings.USER_AGENT
        activityIndicator.color = Settings.LOADING_SIGN_COLOR
        doInjections()
    }
    
    // MARK: - Pull to refresh code
    private func pullToRefresh(){
            self.view.backgroundColor = statusBarColor
            if Settings.PULL_TO_REFRESH {
                    self.refreshControl = UIRefreshControl.init()
                    refreshControl!.bounds = CGRect(x: 0, y: ((refreshControl!.bounds.size.height)-60), width: refreshControl!.bounds.size.width, height: refreshControl!.bounds.size.height)
                        refreshControl?.tintColor = Settings.LOADING_SIGN_COLOR
                    
                    refreshControl!.addTarget(self, action:#selector(refreshControlClicked), for: UIControl.Event.valueChanged)
                    self.webView.scrollView.addSubview(self.refreshControl!)
            }
        }
        
// Pull to refresh method
        @objc func refreshControlClicked(){
            isPulled = true
            print("refresh method called")
            if isConnected() {
                no_internetLabel.isHidden = true
                no_internet.isHidden = true
                
                if wasOffline == true {webContainerLoad();wasOffline = false}else{webView.reload()}
//                let myRequest = URLRequest(url: refreshURL)
//                webView.load(myRequest)
            }
            else{refreshControl?.endRefreshing()}
        }

// MARK: - webview methods
    func webView(_ webView: WKWebView, didCommit navigation: WKNavigation!) {
        if isPulled == false {
            if Settings.LOADING_SIGN{
                activityIndicator.startAnimating()
            }
        }
    }
    
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {

        
        if webView.canGoBack {backButton.isHidden = false} else {backButton.isHidden = true}
        activityIndicator.stopAnimating()
        refreshControl?.endRefreshing()
        isPulled = false
    }
    
    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        activityIndicator.stopAnimating()
        refreshControl?.endRefreshing()
        isPulled = false
    }
    
    func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping () -> Void) {
        let alert = UIAlertController(title: "Alert", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert, animated: true)
        completionHandler()
    }
    
 
// Activity Navigator
    func activityNavigator(){
        if Settings.LOADING_SIGN {
            webView.addSubview(activityIndicator)
            activityIndicator.startAnimating()
            activityIndicator.hidesWhenStopped = true
        }
    }
    
// MARK: - Navigation Handling
    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        var isEmbed = false
        let docExtension = "png, jpeg, jpg, bmp, gif, pdf,doc,docx,ppt,pptx,zip,rar,xls,xlsx,odt,ods,odp,rtf,mp4,mp3,avi,wav,ogg,mov,wmv,csv"
        let pathExtension = navigationAction.request.url?.pathExtension
        let isDownload = (docExtension).localizedCaseInsensitiveContains(pathExtension!)
        let shareURL = navigationAction.request.url
        let urlElements = shareURL?.absoluteString.components(separatedBy: ":") ?? []
        print(urlElements[0])
        
        // connected and valid url
        if isConnected() && ((shareURL?.absoluteString)?.localizedCaseInsensitiveContains("http"))!{
            print("is connected")
            if ((shareURL?.absoluteString)?.localizedCaseInsensitiveContains("embed"))! {
                isEmbed = true
                print("Embeded part is called!!!!!!!!!!")
            }
            if navigationAction.navigationType == .linkActivated {
                webURL = shareURL!.absoluteString
                setClickCountForInterstitial()
            }
            wasOffline = false
            // if url is scanned with QR
            if isScannedURL {
                print("scan url part called")
                isScannedURL = false
                if !Settings.OPEN_SCAN_URL_IN_WEBVIEW, UIApplication.shared.canOpenURL(shareURL!) {
                    activityIndicator.stopAnimating()
                    UIApplication.shared.open(shareURL!)
                    decisionHandler(.cancel)
                }else{
                    decisionHandler(.allow)
                }
            }
            // if external links in browser on
            else if Settings.EXTERNAL_LINKS_IN_BROWSER && !(pathExtension?.localizedCaseInsensitiveContains(docExtension))! {
                print("top of navigation action")
                let isWhiteListed = isLinkWhiteListed(url: shareURL!.absoluteString)
                
                if navigationAction.navigationType == .linkActivated || isMenuLinkTapped {
                    isMenuLinkTapped = false
                      if let url = navigationAction.request.url,
                        let host = url.host, !host.hasPrefix(Settings.HOST),
                         !isDownload, !isWhiteListed, UIApplication.shared.canOpenURL(url) {
                                print("inside the external link")
                                activityIndicator.stopAnimating()
                                UIApplication.shared.open(url)
                                decisionHandler(.cancel)
                      } else {
                                print("Open it locally")
                                if isDownload && !(("mov,avi,wmv,mp4").localizedCaseInsensitiveContains(pathExtension!)){
                                    decisionHandler(.cancel)
                                    activityNavigator()
                                    if let downloadURL = shareURL {downloadFile(shareURL: downloadURL)}
                                }
                                else{decisionHandler(.allow); print("Locally allow part called")}
                            }
                  }
                else{
                    /// if link is whitelisted or internal
                    print("External else part called")
                    if isPulled == false {activityNavigator()}
                    if let url = navigationAction.request.url, let host = url.host, host.hasPrefix(Settings.HOST), !isDownload{
                        decisionHandler(.allow);print("else allow part executed")
                    }
                    else if isDownload{decisionHandler(.allow); webView.goBack(); print("is download refreshed")}
                    else if isEmbed {decisionHandler(.allow)}
                    else if isLaunchURL == true {decisionHandler(.allow); print("is launch called")}
                    else{
                        
                            print(navigationAction.request.url!)
                            decisionHandler(.allow);print("canceler part is called")
                            //activityIndicator.stopAnimating()
                        }
                    
                    }
                
              }
            // if external links in browser off
            else {
                print("This is the executing part")
                if isDownload && !(("mov,avi,wmv,mp4").localizedCaseInsensitiveContains(pathExtension!)){
                    print("downloading part called")
                    decisionHandler(.cancel)
                    activityNavigator()
                    if let downloadURL = shareURL {downloadFile(shareURL: downloadURL)}
                }
                else if let url = navigationAction.request.url, let host = url.host, host.hasPrefix(Settings.HOST), !isDownload
                {
                    decisionHandler(.allow)
                }
                else{
                    if isDownloadLink(url: shareURL!){
                        print("doc download part called")
                        decisionHandler(.cancel)
                        activityIndicator.startAnimating()
                        if let downloadURL = shareURL {downloadFile(shareURL: downloadURL)}
                    }
                    else {
                        decisionHandler(.allow)
                        print("off else part executed")
                        //activityIndicator.stopAnimating()
                    }
                }
            }
        }
        
        // app url or reset link
        else if isConnected() && !((urlElements[0]).localizedCaseInsensitiveContains("http")) && !shareURL!.absoluteString.localizedCaseInsensitiveContains("website"){
            openAppOrClearCache(urlElements, navigationAction, decisionHandler)
        }
            
        // offline local
        else{
            if ((shareURL?.absoluteString)?.localizedCaseInsensitiveContains("http"))! {
                if Settings.EXTERNAL_LINKS_IN_BROWSER {
                    decisionHandler(.cancel)
                    webContainerLoad()
                    wasOffline = true
                }
                else {
                    if !isDownload{webURL = shareURL!.absoluteString}
                    decisionHandler(.cancel); webContainerLoad(); wasOffline = true
                }
            }
            else{decisionHandler(.allow)}
        }
    }
    /// end of decideForNavigationPolicy
    
    // show interstitial add after specified clicks
    func setClickCountForInterstitial(){
        if Settings.INTERSTITIAL_AD {
            clickCount += 1
            if clickCount == Settings.INTERSTITIAL_AD_AFTER_CLICKS {
                showInterstitialAd()
                clickCount = 0
            }
        }
    }
    
    // check for whitelist external link
    func isLinkWhiteListed(url: String) -> Bool{
        var isWhiteListed = false
        Settings.WHITELIST_EXTERNAL_URLS.forEach { (link) in
            let hostPart = link.components(separatedBy: "//")[1]
            if url.contains(hostPart) { isWhiteListed = true }
        }
        return isWhiteListed
    }
    
    // open app, ratedialog or clear cache
    func openAppOrClearCache(_ urlElements: [String], _ navigationAction: WKNavigationAction, _ decisionHandler: @escaping (WKNavigationActionPolicy) -> Void){
        print("else if enterd")
        setClickCountForInterstitial()
        
        let url = navigationAction.request.url!
        
        if urlElements[0] == "reset" {
            WKWebView.clean()           /// clean cache
            decisionHandler(.cancel)
            webView.reload()
        }
        else if urlElements[0] == "ratedialog" {
            if #available( iOS 10.3,*){
                SKStoreReviewController.requestReview()     /// open ratedialog
            }
            decisionHandler(.cancel)
        }
        else if urlElements[0] == "enablepush" {
            enablePush()
            decisionHandler(.cancel)
        }
        else if urlElements[0] == "disablepush" {
            disablePush()
            decisionHandler(.cancel)
        }
        else if urlElements[0] == "qrcode" {
            let qrVC = QrController()
            qrVC.qrDelegate = self
            qrVC.modalPresentationStyle = .fullScreen
            present(qrVC, animated: true, completion: nil)
            decisionHandler(.cancel)
        }
        else if urlElements[0] == "inapp" {
            let indexElement = urlElements[1].split(separator: "t")[1]
            let productIndex = Int(indexElement)
            if let prodIndex = productIndex {
                let productID = Settings.IN_APP_PRODUCT_IDS[prodIndex - 1]
                buyProduct(productId: productID)
            }
            decisionHandler(.cancel)
        }
        else{
            if UIApplication.shared.canOpenURL(url) {
                UIApplication.shared.open(url)          /// open appropriate app
                decisionHandler(.cancel)
            }
            else { decisionHandler(.allow) }
        }
    }
    
    // enable push notification
    func enablePush(){
        let isAllowed = UserDefaults.standard.bool(forKey: "isAllowed")
        if !isAllowed {
            let alert = UIAlertController(title: "Enable notifications!",
                                          message: "To enable notifications, go to Settings and enable notifications for this app.",
                                          preferredStyle: UIAlertController.Style.alert)

            let okAction = UIAlertAction(title: "OK", style: .cancel, handler: nil)
            alert.addAction(okAction)

            let settingsAction = UIAlertAction(title: "Settings", style: .default, handler: { _ in
                // Take the user to Settings app to possibly change permission.
                guard let settingsUrl = URL(string: UIApplication.openSettingsURLString) else { return }
                if UIApplication.shared.canOpenURL(settingsUrl) {
                    UIApplication.shared.open(settingsUrl, completionHandler: { (success) in
                        // Finished opening URL
                    })
                }
            })
            alert.addAction(settingsAction)

            self.present(alert, animated: true, completion: nil)
        } else {
            let alert = UIAlertController(title: "Notifications are enabled.",
                                          message: "",
                                          preferredStyle: UIAlertController.Style.alert)

            let okAction = UIAlertAction(title: "OK", style: .cancel, handler: nil)
            alert.addAction(okAction)
            self.present(alert, animated: true, completion: nil)
        }
    }
    
    // disable push notification
    func disablePush(){
        let isAllowed = UserDefaults.standard.bool(forKey: "isAllowed")
        if isAllowed {
            let alert = UIAlertController(title: "Disable notifications!",
                                          message: "To disable notifications, go to Settings and turn off notifications for this app.",
                                          preferredStyle: UIAlertController.Style.alert)

            let okAction = UIAlertAction(title: "OK", style: .cancel, handler: nil)
            alert.addAction(okAction)

            let settingsAction = UIAlertAction(title: "Settings", style: .default, handler: { _ in
                // Take the user to Settings app to possibly change permission.
                guard let settingsUrl = URL(string: UIApplication.openSettingsURLString) else { return }
                if UIApplication.shared.canOpenURL(settingsUrl) {
                    UIApplication.shared.open(settingsUrl, completionHandler: { (success) in
                        // Finished opening URL
                    })
                }
            })
            alert.addAction(settingsAction)

            self.present(alert, animated: true, completion: nil)
        } else {
            let alert = UIAlertController(title: "Notifications are disabled.",
                                          message: "",
                                          preferredStyle: UIAlertController.Style.alert)

            let okAction = UIAlertAction(title: "OK", style: .cancel, handler: nil)
            alert.addAction(okAction)
            self.present(alert, animated: true, completion: nil)
        }
    }
    
    // check for download link
    func isDownloadLink(url: URL) -> Bool{
        var value = false
        let extensions = ["pdf", "doc", "docx",
                          "ppt","pptx", "zip", "rar", "xls", "xlsx",
                          "odt", "ods", "odp","rtf", "csv", "png", "bmp", "jpeg", "jpg", "gif" ]
        extensions.forEach { (ext) in
            if url.absoluteString.contains(".\(ext)"){
                FileDownload.containedExtension = ext
                value = true
            }
        }
        return value
    }
    
    // file download
    func downloadFile(shareURL: URL){
        print("url: \(shareURL)")
            FileDownload.download(url: shareURL) { (fileUrl) in
                print("response come to closure")
            let controller = UIDocumentInteractionController(url: fileUrl)
            controller.delegate = self
            controller.presentPreview(animated: true)
                self.activityIndicator.stopAnimating()
        }
    }
    
    func fetchProduct(productId: String){
        let productRequest = SKProductsRequest(productIdentifiers: [productId])
        productRequest.delegate = self
        productRequest.start()
    }
    
    func buyProduct(productId: String){
        print("productID: \(productId)")
        if SKPaymentQueue.canMakePayments() {
            // can make payments
            let paymentRequest = SKMutablePayment()
            paymentRequest.productIdentifier = productId
            SKPaymentQueue.default().add(paymentRequest)

        } else {
            // can't make payments
            print("User can't make payments")
        }
    }
    
    func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration, for navigationAction: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        if navigationAction.targetFrame == nil {
   
            if Settings.EXTERNAL_LINKS_IN_BROWSER {
                UIApplication.shared.open(navigationAction.request.url!)
            } else {
                webView.load(navigationAction.request)
            }
        }
        return nil
    }
    
    func documentInteractionControllerViewControllerForPreview(_ controller: UIDocumentInteractionController) -> UIViewController {
        return self
    }
    
    // screen rotation handling
    override func viewWillTransition(to size: CGSize, with coordinator: UIViewControllerTransitionCoordinator) {
        if size.width > size.height {
            if bannerContainer != nil {
                bannerContainer.removeFromSuperview()
            }
        }
        findHeights()
        
        no_internet.frame = CGRect(x: size.width/2 - 55, y: size.height/3, width: 110, height: 70)
        no_internetLabel.frame = CGRect(x: size.width/2 - 125, y: size.height/3 + 80, width: 250, height: 50)
        
        let yPoint = Settings.SHOW_DRAWER ? (statusBarHeight ?? 40) + (navbarHeight ?? 0) : statusBarHeight
        let bottomPadding = Settings.SHOW_BOTTOM_MENU ? ((tabBarHeight ?? 10) + (yPoint ?? 40)) : 0
        
        webViewContainer.frame = CGRect(x: 0, y: yPoint ?? 0, width: size.width, height: size.height - bottomPadding)
        
        
    }
    
    // TabBar item selected
    override func tabBar(_ tabBar: UITabBar, didSelect item: UITabBarItem) {
        let indexOfTab = tabBar.items?.firstIndex(of: item)
        if let index = indexOfTab {
            isMenuLinkTapped = true
            activityIndicator.startAnimating()
            loadWebWithUrlString(url: Settings.BOTTOM_MENU_LINKS[index], webView: webView)
        }
    }
    
// URL Setting
    func createURL(url: String) -> URL{
        if !(url.localizedCaseInsensitiveContains("http")){
            let arr = url.split(separator: ".")
            let ext = arr[1].split(separator: "?")
            return Bundle.main.url(forResource: String(arr[0]), withExtension: String(ext[0]))!
        }else{
            return URL(string: url)!
        }
    }
// Orientation Setup
    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        
        switch orientation {
        case 0:
            return .portrait
        case 1:
            return .landscape
        case 2:
            return .all
        default:
            return .all
        }
    }
        
    override var prefersStatusBarHidden: Bool {
        return false
    }
    
    // Check for internet connection
    func isConnected() -> Bool{
        let connection = ConnectionCheck()
        return connection.checkReachable()
    }
    
    func qrUrlValue(value: String) {
        qrUrl = value
    }
    
    func priceStringForProduct(item: SKProduct) -> String? {
        let price = item.price
        if price == NSDecimalNumber(decimal: 0.00) {
            return "GET" //or whatever you like really... maybe 'Free'
        } else {
            let numberFormatter = NumberFormatter()
            let locale = item.priceLocale
            numberFormatter.numberStyle = .currency
            numberFormatter.locale = locale
            return numberFormatter.string(from: price)
        }
    }
   
}

extension HomeController: OSSubscriptionObserver, SKPaymentTransactionObserver, SKProductsRequestDelegate, GADBannerViewDelegate, GADInterstitialDelegate {
    func productsRequest(_ request: SKProductsRequest, didReceive response: SKProductsResponse) {
        if let product = response.products.first {
            DispatchQueue.main.async {
                let priceString = self.priceStringForProduct(item: product)
                
                let message = product.localizedDescription + "\n\n" + "price: \(priceString ?? "\(product.price)")"
                
                let alert = UIAlertController(title: product.localizedTitle,
                                              message: message,
                                              preferredStyle: UIAlertController.Style.alert)

                let okAction = UIAlertAction(title: "cancel", style: .cancel, handler: nil)
                alert.addAction(okAction)

                let settingsAction = UIAlertAction(title: "Buy", style: .default, handler: { _ in
                    self.buyProduct(productId: product.productIdentifier)
                })
                alert.addAction(settingsAction)

                self.present(alert, animated: true, completion: nil)
            }
        }
    }
    
    func paymentQueue(_ queue: SKPaymentQueue, updatedTransactions transactions: [SKPaymentTransaction]) {
        for transaction in transactions {
            if transaction.transactionState == .purchased {
                // payment successful
                print("Payment is successful!")
                SKPaymentQueue.default().finishTransaction(transaction)
                
            }
            else if transaction.transactionState == .failed {
                // payment failed
                if let error = transaction.error {
                    print("Transaction failed due to error: \(error.localizedDescription)")
                }
                SKPaymentQueue.default().finishTransaction(transaction)
            }
            else if transaction.transactionState == .restored {
                print("In-app purchase is restored")
                SKPaymentQueue.default().finishTransaction(transaction)
            }
        }
    }
    
    func onOSSubscriptionChanged(_ stateChanges: OSSubscriptionStateChanges!) {
        _ = stateChanges.to.userId; //print("playerId: \(playerId)")
    }
    
}


extension WKWebView {
    class func clean() {
        guard #available(iOS 9.0, *) else {return}

        HTTPCookieStorage.shared.removeCookies(since: Date.distantPast)

        WKWebsiteDataStore.default().fetchDataRecords(ofTypes: WKWebsiteDataStore.allWebsiteDataTypes()) { records in
            records.forEach { record in
                WKWebsiteDataStore.default().removeData(ofTypes: record.dataTypes, for: [record], completionHandler: {})
                #if DEBUG
                    print("WKWebsiteDataStore record deleted:", record)
                #endif
            }
        }
    }
}


