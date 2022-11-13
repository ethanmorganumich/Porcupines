import SwiftUI

final class UserState : ObservableObject {
    @Published var view: String;
    @Published var previous_view: String;
    @Published var note_idx: Int;

    static let shared = UserState() // create one instance of the class to be shared
    private init() {
        self.view = ""
        self.previous_view = ""
        self.note_idx = -1
    }
    private let serverUrl = "https://34.134.70.89/"
    @Published private(set) var notes = [Note]()
    private let nFields = Mirror(reflecting: Note()).children.count
    
    func getNotes() {
        guard let apiUrl = URL(string: serverUrl+"notes/") else {
            print("getNotes: Bad URL")
            return
        }
        print("here")
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Accept") // expect response in JSON
        request.httpMethod = "GET"
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            
            guard let data = data, error == nil else {
                print("getNotes: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("getNotes: HTTP STATUS: \(httpStatus.statusCode)")
                return
            }
            
            guard let jsonObj = try? JSONSerialization.jsonObject(with: data) as? [String:Any] else {
                print("getChatts: failed JSON deserialization")
                return
            }
            let notesReceived = jsonObj["notes"] as? [[String:Any]] ?? []
            print(notesReceived)
            DispatchQueue.main.async {
                self.notes = [Note]()
                for (note_idx, noteEntry) in notesReceived.enumerated() {
                    print(noteEntry)
//                    if noteEntry.count == self.nFields {
                        self.notes.append(Note(title: (noteEntry["title"] as! String),
                                               text: (noteEntry["content"] as! String),
                                               timestamp: "timestamp",
                                               idx: note_idx,
                                               id: (noteEntry["note_id"] as! String),
                                               tags: ["test", "tags"]
                                              ))
//                    } else {
//                        print("getNotes: Received unexpected number of fields: \(noteEntry.count) instead of \(self.nFields).")
//                    }
                }
            }
            print(self.notes)
        }.resume()
    }
    
    func viewNote(_ idx: Int) {
        note_idx = idx
        previous_view = view
        view = "existing note view"
    }
    
    func saveNote(_ note: Note, _ updated_title: String, _ updated_content: String) {
        let jsonObj = ["title": updated_title,
                       "content": updated_content]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("postNote: jsonData serialization error")
            return
        }
        
        guard let apiUrl = URL(string: serverUrl+"notes/"+note.id!) else {
            print("postNote: Bad URL")
            return
        }
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "UPDATE"
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("postNote: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("postNote: HTTP STATUS: \(httpStatus.statusCode)")
                    return
                } else {
                    self.getNotes()
                }
            }
        }.resume()
    }
    
    func createNote(_ title: String, _ content: String) {
        let jsonObj = ["title": title,
                       "content": content]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("postNote: jsonData serialization error")
            return
        }
        
        guard let apiUrl = URL(string: serverUrl+"notes/") else {
            print("postNote: Bad URL")
            return
        }
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("postNote: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("postNote: HTTP STATUS: \(httpStatus.statusCode)")
                    return
                } else {
                    self.getNotes()
                }
            }
        }.resume()
    }
    
    func deleteNote() {
        
        guard let apiUrl = URL(string: serverUrl+"notes/"+self.notes[self.note_idx].id!) else {
            print("postNote: Bad URL")
            return
        }
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "DELETE"
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("postNote: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("postNote: HTTP STATUS: \(httpStatus.statusCode)")
                    return
                } else {
                    self.getNotes()
                }
            }
        }.resume()
    }
}
