//
//  ContainerController.swift
//  Convertify
//
//  Created by apple on 8/6/20.
//  Copyright © 2020 apple001. All rights reserved.
//

import UIKit

var isExpanded = false

class ContainerController: UIViewController, UIGestureRecognizerDelegate {
    // MARK: - properties
    var menuController: MenuController!
    var centerController: UINavigationController!
    var homeController: HomeController!
    private var gifLoader: UIImageView!
    var passingURL: String?
    
    // MARK: - Init
    override func viewDidLoad() {
        super.viewDidLoad()
        setGifView()
        initViews()
    }
    
    // MARK: - Handlers
    private func setGifView(){
        gifLoader = UIImageView()
        view.addSubview(gifLoader)
        gifLoader.placeIn(superView: view)
        gifLoader.contentMode = .scaleAspectFit
        gifLoader.loadGif(name: "animatedText")
    }
    
    private func initViews(){
        if Settings.SHOW_GIF_ANIMATION {
            DispatchQueue.main.asyncAfter(deadline: .now()+Settings.GIF_LOAD_MAX_SECONDS) {
                self.gifLoader.removeFromSuperview()
                self.initiateViews()
            }
        } else {
            self.gifLoader.removeFromSuperview()
            initiateViews()
        }
    }
    
    private func initiateViews(){
        self.configureHomeController()
        self.centerController.navigationBar.barTintColor = Settings.TITLEBAR_BACKGROUND_COLOR
        self.view.backgroundColor = .gray
        self.centerController.navigationBar.isHidden = !Settings.SHOW_DRAWER
        let textAttributes = [NSAttributedString.Key.foregroundColor:Settings.TITLEBAR_TINT_COLOR == "white" ? UIColor.white : UIColor.black]
        self.centerController.navigationBar.titleTextAttributes = textAttributes
        if homeController != nil && passingURL != nil {
            homeController.passedUrl = passingURL
        }
    }
    
    func configureHomeController(){
        homeController = HomeController()
        homeController.homeDelegate = self
        centerController = UINavigationController(rootViewController: homeController)
        view.addSubview(centerController.view)
        addChild(centerController)
        centerController.didMove(toParent: self)
    }
    
    override var preferredStatusBarUpdateAnimation: UIStatusBarAnimation {
        return .slide
    }
    
    // Status Bar Text Color
    override var preferredStatusBarStyle: UIStatusBarStyle {
        switch Settings.STATUS_BAR_TEXT_COLOR {
        case 0:
            return .lightContent
        case 1:
            return .default
        default:
            return .default
        }
    }
    
    override var prefersStatusBarHidden: Bool {
        return false
    }
    
    func configureMenuController(){
        if menuController == nil {
            print("menu controlelr added")
            menuController = MenuController()
            menuController.delegate = self
            view.insertSubview(menuController.view, at: 1)
            addChild(menuController)
            menuController.didMove(toParent: self)
            menuController.view.frame.size.width = view.frame.width - 80
            menuController.view.frame.origin.x = -(view.frame.width - 80)
        }
    }
    
    // show side menu
    func showMenuController(shouldExpand: Bool, index: Int?){
        if shouldExpand {
            // show menu
            UIView.animate(withDuration: 0.5, delay: 0, options: .curveEaseInOut, animations: {
                self.menuController.view.frame.origin.x = 0
            }, completion: nil)
        } else {
            // hide menu
            UIView.animate(withDuration: 0.5, delay: 0, options: .curveEaseInOut, animations: {
                self.menuController.view.frame.origin.x = -(self.view.frame.width - 80)
            }, completion: nil)
            if let ind = index {
                self.didSelectMenuOption(index: ind)
            }
        }
        animateStatusBar()
    }
    
    // selected menu
    func didSelectMenuOption(index: Int){
        homeController.menuURL = Settings.DRAWER_LINKS[index]
    }
    
    func animateStatusBar(){
        UIView.animate(withDuration: 0.5, delay: 0, options: .curveEaseInOut, animations: {
            self.setNeedsStatusBarAppearanceUpdate()
        }, completion: nil)
    }
    
}

extension ContainerController: HomeControllerDelegate {
    func handleMenuToggle(forIndex index: Int?) {
        if !isExpanded {
            configureMenuController()
        }
        isExpanded = !isExpanded
        showMenuController(shouldExpand: isExpanded, index: index)
    }
    
}
