//
//  Utils.swift
//  Convertify
//
//  Created by apple on 8/7/20.
//  Copyright © 2020 apple001. All rights reserved.
//

import UIKit
import WebKit

func loadWebWithUrlString(url: String, webView: WKWebView){
    let myURL = makeURL(url: url)
    let myRequest = URLRequest(url: myURL)
    webView.load(myRequest)
}

func makeURL(url: String) -> URL{
    if !(url.localizedCaseInsensitiveContains("http")){
        let arr = url.split(separator: ".")
        let ext = arr[1].split(separator: "?")
        return Bundle.main.url(forResource: String(arr[0]), withExtension: String(ext[0]))!
    }else{
        return URL(string: url)!
    }
}

func setButtonProperties(target: Any?, button: UIButton, image: String, objFunc: Selector){
    button.setImage(UIImage(named: image), for: .normal)
    button.addTarget(target, action: objFunc, for: .touchUpInside)
    button.tintColor = Settings.TITLEBAR_TINT_COLOR == "white" ? UIColor.white : UIColor.black
}

func setBarItemProperties(item: UIBarButtonItem){
    item.customView?.translatesAutoresizingMaskIntoConstraints = false
    item.customView?.heightAnchor.constraint(equalToConstant: 30).isActive = true
    item.customView?.widthAnchor.constraint(equalToConstant: 30).isActive = true
}

func calculateBannerHeight() -> CGFloat {
    
    if UIApplication.shared.statusBarOrientation.isPortrait {
        switch UIScreen.main.bounds.height {
        case 0 ..< 400: return 32
        case 400 ..< 720: return 50
        case 720...: return 90
        default: return 60
        }
    } else {
        switch UIScreen.main.bounds.width {
        case 0 ..< 400: return 25
        case 400 ..< 720: return 35
        case 720...: return 50
        default: return 50
        }
    }
}
