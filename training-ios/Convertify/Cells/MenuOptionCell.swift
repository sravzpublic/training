//
//  MenuOptionCell.swift
//  Convertify
//
//  Created by apple on 8/6/20.
//  Copyright © 2020 apple001. All rights reserved.
//

import UIKit

class MenuOptionCell: UITableViewCell {

    // MARK: - Properties
    let iconImageView: UIImageView = {
        let imgView = UIImageView()
        imgView.clipsToBounds = true
        return imgView
    }()
    
    let descriptionLabel: UILabel = {
        let label = UILabel()
        label.textColor = .white
        label.font = UIFont.systemFont(ofSize: 16)
        label.text = "Dummy"
        return label
    }()
    
    // MARK: - Init
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        backgroundColor = Settings.DRAWER_BACKGROUND_COLOR
        
        addSubview(iconImageView)
        iconImageView.tintColor = Settings.DRAWER_ICON_COLOR
        iconImageView.inMiddleLeftOf(superview: self, width: Settings.SHOW_DRAWER_ICONS ? 25 : 0, height: 20, paddingLeft: Settings.SHOW_DRAWER_ICONS ? 10 : 0)
        
        addSubview(descriptionLabel)
        descriptionLabel.textColor = Settings.DRAWER_TITLE_COLOR
        descriptionLabel.onRightSideOf(subview: iconImageView, width: 100, height: 20, paddingLeft: 15)
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    // MARK: - Handlers

}
