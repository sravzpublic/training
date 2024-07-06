
import Foundation

class FileDownload {
    
    public static var fileURL:URL?
    public static var isComplete = false
    public static var containedExtension = ""
    public static func download(url: URL, completion: @escaping (URL) -> Void){
        
        let fileExtension = url.pathExtension == "" ? containedExtension : url.pathExtension
        
        let destination: DownloadRequest.Destination = { _, _ in
                let documentsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
                let fileURL = documentsURL.appendingPathComponent("file.\(fileExtension)")

                return (fileURL, [.removePreviousFile, .createIntermediateDirectories])
            }
            
            AF.download(url, to: destination).response { response in
                debugPrint(response)

                if response.error == nil {
                    completion(response.fileURL!)
                }
            }
        
    }
  
}
