//
//  Extensions.swift
//  Convertify
//
//  Created by apple on 8/6/20.
//  Copyright © 2020 apple001. All rights reserved.
//
import UIKit

extension UIView {
    func placeIn(superView: UIView, paddingTop: CGFloat = 0, paddingLeft: CGFloat = 0, paddingRight: CGFloat = 0, paddingBottom: CGFloat = 0, isSafeArea: Bool = false) {
        translatesAutoresizingMaskIntoConstraints = false
        if isSafeArea {
            if #available(iOS 11.0, *) {
                topAnchor.constraint(equalTo: superView.safeAreaLayoutGuide.topAnchor, constant: paddingTop).isActive = true
            } else {
                    topAnchor.constraint(equalTo: superView.topAnchor, constant: paddingTop).isActive = true
            }
        } else {
            topAnchor.constraint(equalTo: superView.topAnchor, constant: paddingTop).isActive = true
        }
        leadingAnchor.constraint(equalTo: superView.leadingAnchor, constant: paddingLeft).isActive = true
        trailingAnchor.constraint(equalTo: superView.trailingAnchor, constant: -paddingRight).isActive = true
        if isSafeArea {
            if #available(iOS 11.0, *) {
                bottomAnchor.constraint(equalTo: superView.bottomAnchor, constant: -paddingBottom).isActive = true
            } else {
                bottomAnchor.constraint(equalTo: superView.bottomAnchor, constant: -paddingBottom).isActive = true
            }
        } else {
            bottomAnchor.constraint(equalTo: superView.bottomAnchor, constant: -paddingBottom).isActive = true
        }
    }
    
    func inMiddleLeftOf(superview: UIView, width: CGFloat, height: CGFloat, paddingLeft: CGFloat){
        setWidthHeight(width: width, height: height)
        centerYAnchor.constraint(equalTo: superview.centerYAnchor).isActive = true
        leftAnchor.constraint(equalTo: superview.leftAnchor, constant: paddingLeft).isActive = true
    }
    
    func onRightSideOf(subview: UIView, width: CGFloat, height: CGFloat, isVerticallyCenter: Bool = false, paddingTop: CGFloat = 0, paddingLeft: CGFloat = 0){
        setWidthHeight(width: width, height: height)
        
        if isVerticallyCenter {
            centerYAnchor.constraint(equalTo: subview.centerYAnchor).isActive = true
        } else {
            topAnchor.constraint(equalTo: subview.topAnchor, constant: paddingTop).isActive = true
        }
        
        leftAnchor.constraint(equalTo: subview.rightAnchor, constant: paddingLeft).isActive = true
    }
    
    func anchorToTopLeftRightWith(height: CGFloat, toView: UIView, paddingTop: CGFloat = 0, paddingLeft: CGFloat = 0, paddingRight: CGFloat = 0){
        translatesAutoresizingMaskIntoConstraints = false
        if #available(iOS 11.0, *) {
            topAnchor.constraint(equalTo: toView.safeAreaLayoutGuide.topAnchor, constant: paddingTop).isActive = true
        } else {
            topAnchor.constraint(equalTo: toView.topAnchor, constant: paddingTop).isActive = true
        }
        leadingAnchor.constraint(equalTo: toView.leadingAnchor, constant: paddingLeft).isActive = true
        trailingAnchor.constraint(equalTo: toView.trailingAnchor, constant: -paddingRight).isActive = true
        heightAnchor.constraint(equalToConstant: height).isActive = true
    }
    
    func inCenterOf(superview: UIView, width: CGFloat, height: CGFloat){
        setWidthHeight(width: width, height: height)
        
        centerXAnchor.constraint(equalTo: superview.centerXAnchor).isActive = true
        centerYAnchor.constraint(equalTo: superview.centerYAnchor).isActive = true
    }
    
    // under the view or below the relative view
    func underThe(subview: UIView, height: CGFloat, paddingTop: CGFloat = 0, paddingLeft: CGFloat = 0, paddingRight: CGFloat = 0){
        translatesAutoresizingMaskIntoConstraints = false
        topAnchor.constraint(equalTo: subview.bottomAnchor, constant: paddingTop).isActive = true
        leftAnchor.constraint(equalTo: subview.leftAnchor, constant: paddingLeft).isActive = true
        rightAnchor.constraint(equalTo: subview.rightAnchor, constant: paddingRight).isActive = true
        heightAnchor.constraint(equalToConstant: height).isActive = true
    }
    
    private func setWidthHeight(width: CGFloat, height: CGFloat) {
        translatesAutoresizingMaskIntoConstraints = false
        widthAnchor.constraint(equalToConstant: width).isActive = true
        heightAnchor.constraint(equalToConstant: height).isActive = true
    }
}

extension UIDevice {
    var hasNotch: Bool {
        var bottom: CGFloat = 0
        if #available(iOS 11.0, *) {
            bottom = UIApplication.shared.keyWindow?.safeAreaInsets.bottom ?? 0
        } else {
            // Fallback on earlier versions
        }
        return bottom > 0
    }
}

