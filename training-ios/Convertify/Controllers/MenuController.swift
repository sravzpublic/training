//
//  MenuController.swift
//  Convertify
//
//  Created by apple on 8/6/20.
//  Copyright © 2020 apple001. All rights reserved.
//

import UIKit

let reuseIdentifier = "MenuOptionCell"

class MenuController: UIViewController {
    // MARK: - properties
    var tableView: UITableView!
    var delegate: HomeControllerDelegate?
    
    // MARK: - Init
    override func viewDidLoad() {
        super.viewDidLoad()
        configureTableView()
    }
    
    // MARK: - Handlers
    func configureTableView(){
        tableView = UITableView()
        tableView.delegate = self
        tableView.dataSource = self
        tableView.backgroundColor = Settings.DRAWER_BACKGROUND_COLOR
        view.addSubview(tableView)
        tableView.separatorStyle = .none
        tableView.rowHeight = 60
        
        tableView.register(MenuOptionCell.self, forCellReuseIdentifier: reuseIdentifier)
        tableView.placeIn(superView: view)

    }
    
}

extension MenuController: UITableViewDelegate, UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        Settings.DRAWER_TITLES.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: reuseIdentifier, for: indexPath) as! MenuOptionCell
        
        cell.iconImageView.image = UIImage(named: Settings.DRAWER_ICONS[indexPath.row])
        cell.descriptionLabel.text = Settings.DRAWER_TITLES[indexPath.row]
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        delegate?.handleMenuToggle(forIndex: indexPath.row)
    }
    
}
