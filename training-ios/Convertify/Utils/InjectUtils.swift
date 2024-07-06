//
//  InjectUtils.swift
//  Convertify
//
//  Created by apple on 7/11/20.
//  Copyright © 2020 apple001. All rights reserved.
//

import UIKit
import WebKit

/// MARK: - Reading contents of files
private func readFileBy(name: String, type: String) -> String {
    guard let path = Bundle.main.path(forResource: name, ofType: type) else {
        return "Failed to find path"
    }
    
    do {
        return try String(contentsOfFile: path, encoding: .utf8)
    } catch {
        return "Unkown Error"
    }
}

/// MARK: - Inject to web page
func injectCssToPage(webView: WKWebView, name: String) {
    let cssFile = readFileBy(name: name, type: "css")
    
    let cssStyle = """
        javascript:(function() {
        var parent = document.getElementsByTagName('head').item(0);
        var style = document.createElement('style');
        style.type = 'text/css';
        style.innerHTML = window.atob('\(encodeStringTo64(fromString: cssFile)!)');
        parent.appendChild(style)})()
    """

    let cssScript = WKUserScript(source: cssStyle, injectionTime: .atDocumentEnd, forMainFrameOnly: false)
    webView.configuration.userContentController.addUserScript(cssScript)
}

/// MARK: - Inject to web page
func injectJsToPage(webView: WKWebView, name: String) {
    let jsFile = readFileBy(name: name, type: "js")
        
    let jsStyle = """
        javascript:(function() {
        var parent = document.getElementsByTagName('head').item(0);
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.innerHTML = window.atob('\(encodeStringTo64(fromString: jsFile)!)');
        parent.appendChild(script)})()
    """

    let jsScript = WKUserScript(source: jsStyle, injectionTime: .atDocumentEnd, forMainFrameOnly: false)
    
    webView.configuration.userContentController.addUserScript(jsScript)
}

// 4
// MARK: - Encode string to base 64
private func encodeStringTo64(fromString: String) -> String? {
    let plainData = fromString.data(using: .utf8)
    return plainData?.base64EncodedString(options: [])
}
