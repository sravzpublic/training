//
//  ConnectionCheck.swift
//  Convertify
//
//  Created by apple on 10/13/19.
//  Copyright © 2019 apple001. All rights reserved.
//

import Foundation
import SystemConfiguration

class ConnectionCheck{
    private let reachability = SCNetworkReachabilityCreateWithName(nil, "www.google.com")
    
    public func checkReachable() -> Bool{
        var flags = SCNetworkReachabilityFlags()
        SCNetworkReachabilityGetFlags(self.reachability!, &flags)
        if (isNetworkReach(with: flags)){
            return true
        }
        return false
    }
    
    private func isNetworkReach(with flags:SCNetworkReachabilityFlags) -> Bool{
        let isReachable = flags.contains(.reachable)
        return isReachable
    }
}
